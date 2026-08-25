"""A dependency-free reader for the YAML subset used by this repository.

Why this exists
---------------
The setup and validation scripts have to run on a Team Leader's laptop with
nothing installed. PyYAML is not part of the Python standard library, and
telling a non-engineer to `pip install` something before they can validate their
own config is a bad first experience.

So: if PyYAML is available we use it (see ``load``). If it is not, we fall back
to this reader, which handles exactly the subset of YAML that this repository's
config files use:

    key: value                  scalars: str, int, float, bool, null
    key:                        nested mappings by indentation
      nested: value
    key: [a, b, c]              inline flow sequences of scalars
    key: {}                     empty inline mapping
    - item                      block sequences of scalars
    - key: value                block sequences of mappings
      other: value
    key: |                      literal block scalars (newlines preserved)
    key: >                      folded block scalars (newlines become spaces)
      with |- >- |+ >+ chomping indicators
    # comments, and blank lines

It deliberately does NOT support anchors, aliases, multiple documents,
complex keys, or nested flow collections.
If you add one of those to a config file, this reader will raise rather than
silently misparse it. That is the intended behavior.
"""

from __future__ import annotations

import json
import re


class MiniYamlError(ValueError):
    """Raised when input falls outside the supported YAML subset."""


_UNSUPPORTED = ("|", ">", "&", "*", "?", "---", "...")


def load(text: str):
    """Parse *text*. Uses PyYAML when installed, otherwise the subset reader."""
    try:
        import yaml  # type: ignore
    except ImportError:
        return loads_subset(text)
    return yaml.safe_load(text)


def load_file(path):
    with open(path, "r", encoding="utf-8") as fh:
        return load(fh.read())


# --------------------------------------------------------------------------
# Subset reader
# --------------------------------------------------------------------------

_BLOCK_SCALAR = re.compile(
    r"^(?P<indent>\s*)(?P<key>(?:\"[^\"]*\"|'[^']*'|[^:#\s][^:]*?))\s*:"
    r"\s*(?P<style>[|>])(?P<chomp>[-+]?)\s*(?:#.*)?$"
)


def _fold_block_scalars(text: str) -> str:
    """Rewrite ``key: |`` / ``key: >`` blocks as single double-quoted scalars.

    Doing this as a pre-pass means the tokenizer never has to know that some
    lines are literal content rather than structure — which matters because
    a ``#`` inside a literal block is text, not a comment.
    """
    lines = text.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        match = _BLOCK_SCALAR.match(lines[i])
        if not match:
            out.append(lines[i])
            i += 1
            continue

        indent = len(match.group("indent"))
        style, chomp = match.group("style"), match.group("chomp")

        body: list[str] = []
        i += 1
        while i < len(lines):
            line = lines[i]
            if not line.strip():
                body.append("")
                i += 1
                continue
            if len(line) - len(line.lstrip(" ")) <= indent:
                break
            body.append(line)
            i += 1

        content_lines = [ln for ln in body if ln.strip()]
        pad = min((len(ln) - len(ln.lstrip(" ")) for ln in content_lines), default=0)
        body = [ln[pad:] if ln.strip() else "" for ln in body]

        while body and not body[-1]:
            body.pop()

        if style == "|":
            value = "\n".join(body)
        else:
            # Folded: join runs of non-blank lines with spaces; a blank line
            # becomes a single newline.
            parts, run = [], []
            for line in body:
                if line:
                    run.append(line.strip())
                else:
                    parts.append(" ".join(run))
                    run = []
            parts.append(" ".join(run))
            value = "\n".join(parts)

        if chomp == "+":
            value += "\n"
        elif chomp != "-":
            value += "\n" if body else ""
            value = value.rstrip("\n") + ("\n" if body else "")
            if style == ">" or style == "|":
                value = value.rstrip("\n")

        out.append(f"{match.group('indent')}{match.group('key')}: {json.dumps(value)}")
    return "\n".join(out)


def loads_subset(text: str):
    lines = _significant_lines(_fold_block_scalars(text))
    if not lines:
        return None
    value, index = _parse_block(lines, 0, lines[0][0])
    if index != len(lines):
        raise MiniYamlError(
            f"line {lines[index][2]}: unexpected indentation, could not continue parsing"
        )
    return value


def _significant_lines(text: str):
    """Return [(indent, content, line_number)] with comments and blanks removed."""
    out = []
    for number, raw in enumerate(text.splitlines(), start=1):
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("---") or stripped.startswith("..."):
            raise MiniYamlError(f"line {number}: multi-document YAML is not supported")
        content = _strip_comment(raw).rstrip()
        if not content.strip():
            continue
        indent = len(content) - len(content.lstrip(" "))
        if "\t" in raw[:indent]:
            raise MiniYamlError(f"line {number}: tabs cannot be used for indentation")
        out.append((indent, content.strip(), number))
    return out


def _strip_comment(line: str) -> str:
    """Remove a trailing ``#`` comment, respecting quotes."""
    quote = None
    for i, ch in enumerate(line):
        if quote:
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
        elif ch == "#" and (i == 0 or line[i - 1] in " \t"):
            return line[:i]
    return line


def _parse_block(lines, index: int, indent: int):
    """Parse a mapping or sequence at *indent*, starting at *index*."""
    if lines[index][1].startswith("- "):
        return _parse_sequence(lines, index, indent)
    return _parse_mapping(lines, index, indent)


def _parse_mapping(lines, index: int, indent: int):
    result = {}
    while index < len(lines):
        line_indent, content, number = lines[index]
        if line_indent < indent:
            break
        if line_indent > indent:
            raise MiniYamlError(f"line {number}: unexpected indentation in mapping")
        if content.startswith("- "):
            break

        key, _, rest = content.partition(":")
        if not _:
            raise MiniYamlError(f"line {number}: expected 'key: value'")
        key = _scalar(key.strip(), number)
        rest = rest.strip()
        index += 1

        if rest:
            result[key] = _scalar(rest, number)
            continue

        # Value is on following, more-indented lines (or absent -> None).
        if index < len(lines) and lines[index][0] > line_indent:
            result[key], index = _parse_block(lines, index, lines[index][0])
        elif index < len(lines) and lines[index][0] == line_indent and lines[index][1].startswith("- "):
            # A block sequence may sit at the same indent as its key.
            result[key], index = _parse_sequence(lines, index, line_indent)
        else:
            result[key] = None
    return result, index


def _parse_sequence(lines, index: int, indent: int):
    result = []
    while index < len(lines):
        line_indent, content, number = lines[index]
        if line_indent < indent or not content.startswith("- "):
            break
        if line_indent > indent:
            raise MiniYamlError(f"line {number}: unexpected indentation in sequence")

        item = content[2:].strip()
        index += 1

        # "- key: value" begins a mapping whose remaining keys are indented
        # to the column just past the dash.
        if _looks_like_mapping_entry(item):
            child_indent = indent + 2
            synthetic = [(child_indent, item, number)]
            while index < len(lines) and lines[index][0] >= child_indent and not (
                lines[index][0] == child_indent and lines[index][1].startswith("- ")
            ):
                synthetic.append(lines[index])
                index += 1
            value, consumed = _parse_mapping(synthetic, 0, child_indent)
            if consumed != len(synthetic):
                raise MiniYamlError(f"line {number}: could not fully parse sequence item")
            result.append(value)
        elif item:
            result.append(_scalar(item, number))
        elif index < len(lines) and lines[index][0] > indent:
            value, index = _parse_block(lines, index, lines[index][0])
            result.append(value)
        else:
            result.append(None)
    return result, index


_MAPPING_ENTRY = re.compile(r"^(?:\"[^\"]*\"|'[^']*'|[^:\s\"'][^:]*?)\s*:(?:\s|$)")


def _looks_like_mapping_entry(item: str) -> bool:
    return bool(_MAPPING_ENTRY.match(item))


_INT = re.compile(r"^[-+]?\d+$")
_FLOAT = re.compile(r"^[-+]?(?:\d+\.\d*|\.\d+)(?:[eE][-+]?\d+)?$")


def _scalar(token: str, number: int):
    token = token.strip()
    if not token:
        return None

    if len(token) >= 2 and token[0] == token[-1] and token[0] in "\"'":
        if token[0] == '"' and "\\" in token:
            try:
                return json.loads(token)
            except ValueError:
                pass
        return token[1:-1]

    if token == "{}":
        return {}
    if token == "[]":
        return []
    if token.startswith("[") and token.endswith("]"):
        inner = token[1:-1].strip()
        if not inner:
            return []
        if "[" in inner or "{" in inner:
            raise MiniYamlError(f"line {number}: nested flow collections are not supported")
        return [_scalar(part, number) for part in _split_flow(inner)]
    if token.startswith("{"):
        raise MiniYamlError(f"line {number}: inline mappings other than {{}} are not supported")

    if token in _UNSUPPORTED or token[0] in "|>&*":
        raise MiniYamlError(f"line {number}: unsupported YAML construct {token!r}")

    lowered = token.lower()
    if lowered in ("true", "yes", "on"):
        return True
    if lowered in ("false", "no", "off"):
        return False
    if lowered in ("null", "~"):
        return None
    if _INT.match(token):
        return int(token)
    if _FLOAT.match(token):
        return float(token)
    return token


def _split_flow(inner: str):
    """Split a flow sequence body on commas that are outside quotes."""
    parts, buf, quote = [], [], None
    for ch in inner:
        if quote:
            buf.append(ch)
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
            buf.append(ch)
        elif ch == ",":
            parts.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    if buf:
        parts.append("".join(buf))
    return [p.strip() for p in parts if p.strip()]
