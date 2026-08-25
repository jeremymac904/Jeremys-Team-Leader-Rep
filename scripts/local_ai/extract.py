#!/usr/bin/env python3
"""Local document extraction. Everything here runs on this machine.

The cheapest method that works is always tried first, because handing a raw
scanned PDF to a vision model for every page is slow and less accurate than
reading a text layer that is already there.

    native text  ->  tables  ->  OCR  ->  page images for a vision model

    python3 scripts/local_ai/extract.py <file>
    python3 scripts/local_ai/extract.py <file> --json
    python3 scripts/local_ai/extract.py <file> --classify-only

Supported: PDF (native text and scanned), DOCX, XLSX, and images.

Nothing in this module makes a network call. That is deliberate and is what
lets Local Privacy Mode make an honest promise about extraction.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
from miniyaml import load_file  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
CONFIG = ROOT / "config" / "local-ai.yaml"
CONFIG_EXAMPLE = ROOT / "config" / "local-ai.example.yaml"

# Signals used to classify a document from its own text.
DOC_SIGNATURES = [
    ("paystub", ("earnings statement", "pay stub", "paystub", "pay period", "ytd",
                 "gross pay", "net pay", "year to date")),
    ("w2", ("w-2", "wage and tax statement", "form w-2", "social security wages",
            "medicare wages")),
    ("tax_return", ("form 1040", "u.s. individual income tax return", "schedule c",
                    "schedule e", "adjusted gross income", "taxable income")),
    ("bank_statement", ("account summary", "beginning balance", "ending balance",
                        "statement period", "deposits and additions", "withdrawals")),
    ("purchase_contract", ("purchase and sale", "purchase agreement", "earnest money",
                           "seller", "buyer", "closing date", "contingency")),
    ("loan_estimate", ("loan estimate", "estimated cash to close", "loan terms",
                       "projected payments", "closing cost details")),
    ("closing_disclosure", ("closing disclosure", "cash to close", "loan costs",
                            "summaries of transactions")),
    ("mortgage_statement", ("mortgage statement", "principal balance", "escrow balance",
                            "payment due date", "amount due")),
    ("appraisal", ("uniform residential appraisal", "appraised value", "comparable sale",
                   "subject property")),
    ("insurance", ("declarations page", "policy number", "coverage", "premium",
                   "dwelling coverage")),
    ("hoa", ("homeowners association", "hoa", "assessment", "covenants")),
    ("1099", ("form 1099", "1099-misc", "1099-nec", "nonemployee compensation")),
]


@dataclass
class PageResult:
    page: int
    method: str                      # native | ocr | image-only
    char_count: int
    text: str = ""
    needs_vision: bool = False


@dataclass
class ExtractionResult:
    source_file: str
    file_type: str
    processed_locally: bool = True
    document_type: str = "unknown"
    classification_confidence: str = "low"
    page_count: int = 0
    pages: list = field(default_factory=list)
    tables: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    methods_used: list = field(default_factory=list)
    full_text: str = ""


def load_config() -> dict:
    return load_file(CONFIG if CONFIG.exists() else CONFIG_EXAMPLE) or {}


def classify(text: str) -> tuple[str, str]:
    """Guess the document type from its text. Returns (type, confidence)."""
    low = (text or "").lower()
    if not low.strip():
        return "unknown", "none"
    scores = {}
    for doc_type, markers in DOC_SIGNATURES:
        hits = sum(1 for m in markers if m in low)
        if hits:
            scores[doc_type] = hits
    if not scores:
        return "unknown", "none"
    best = max(scores, key=scores.get)
    hits = scores[best]
    runner_up = sorted(scores.values(), reverse=True)
    ambiguous = len(runner_up) > 1 and runner_up[1] == hits
    if hits >= 3 and not ambiguous:
        return best, "high"
    if hits >= 2:
        return best, "moderate"
    return best, "low"


# --------------------------------------------------------------------------
# PDF
# --------------------------------------------------------------------------

def extract_pdf(path: Path, config: dict) -> ExtractionResult:
    import pymupdf

    docs_cfg = config.get("documents") or {}
    ocr_cfg = docs_cfg.get("ocr") or {}
    min_native = int(docs_cfg.get("min_chars_for_native") or ocr_cfg.get("min_chars_for_native") or 100)
    max_pages = int(docs_cfg.get("max_pages_per_document") or 50)
    dpi = int(docs_cfg.get("render_dpi") or 200)
    ocr_enabled = bool(ocr_cfg.get("enabled", True))

    result = ExtractionResult(source_file=str(path.name), file_type="pdf")
    doc = pymupdf.open(path)
    result.page_count = doc.page_count

    if doc.page_count > max_pages:
        result.warnings.append(
            f"Document has {doc.page_count} pages; only the first {max_pages} were processed "
            f"(max_pages_per_document in config/local-ai.yaml)."
        )

    ocr_available = bool(shutil.which("tesseract"))
    if ocr_enabled and not ocr_available:
        result.warnings.append(
            "OCR is enabled but tesseract is not installed. Scanned pages could not be read. "
            "Install it with: brew install tesseract"
        )

    for index in range(min(doc.page_count, max_pages)):
        page = doc[index]
        text = page.get_text().strip()

        if len(text) >= min_native:
            result.pages.append(PageResult(index + 1, "native", len(text), text))
            continue

        # Not enough text: this page is scanned or image-only.
        if ocr_enabled and ocr_available:
            try:
                import pytesseract
                from PIL import Image
                import io

                pix = page.get_pixmap(dpi=dpi)
                image = Image.open(io.BytesIO(pix.tobytes("png")))
                ocr_text = pytesseract.image_to_string(image).strip()
                result.pages.append(PageResult(index + 1, "ocr", len(ocr_text), ocr_text))
                if len(ocr_text) < min_native:
                    result.warnings.append(
                        f"Page {index + 1}: OCR produced very little text ({len(ocr_text)} chars). "
                        f"The scan may be poor quality — verify this page by hand."
                    )
            except Exception as exc:  # noqa: BLE001 - report, never fall back to cloud
                result.pages.append(PageResult(index + 1, "image-only", 0, "", needs_vision=True))
                result.warnings.append(f"Page {index + 1}: local OCR failed ({exc}). "
                                       f"This page needs the local vision model.")
        else:
            result.pages.append(PageResult(index + 1, "image-only", 0, "", needs_vision=True))

    # Tables, from pages that had a real text layer.
    try:
        import pdfplumber
        with pdfplumber.open(path) as pdf:
            for index, page in enumerate(pdf.pages[:max_pages]):
                for table in page.extract_tables() or []:
                    cleaned = [[(c or "").strip() for c in row] for row in table if any(row)]
                    if len(cleaned) > 1:
                        result.tables.append({"page": index + 1, "rows": cleaned})
    except Exception as exc:  # noqa: BLE001
        result.warnings.append(f"Table extraction did not run: {exc}")

    doc.close()
    _finalize(result)
    return result


# --------------------------------------------------------------------------
# Other formats
# --------------------------------------------------------------------------

def extract_docx(path: Path, config: dict) -> ExtractionResult:
    import docx

    result = ExtractionResult(source_file=path.name, file_type="docx")
    document = docx.Document(path)
    text = "\n".join(p.text for p in document.paragraphs if p.text.strip())
    result.pages.append(PageResult(1, "native", len(text), text))
    result.page_count = 1
    for table in document.tables:
        rows = [[cell.text.strip() for cell in row.cells] for row in table.rows]
        if len(rows) > 1:
            result.tables.append({"page": 1, "rows": rows})
    _finalize(result)
    return result


def extract_xlsx(path: Path, config: dict) -> ExtractionResult:
    import openpyxl

    result = ExtractionResult(source_file=path.name, file_type="xlsx")
    book = openpyxl.load_workbook(path, data_only=True)
    chunks = []
    for sheet in book.worksheets:
        rows = [[("" if c is None else str(c)) for c in row]
                for row in sheet.iter_rows(values_only=True)]
        rows = [r for r in rows if any(v.strip() for v in r)]
        if rows:
            result.tables.append({"sheet": sheet.title, "rows": rows})
            chunks.append(f"[{sheet.title}]\n" + "\n".join("\t".join(r) for r in rows))
    text = "\n\n".join(chunks)
    result.pages.append(PageResult(1, "native", len(text), text))
    result.page_count = 1
    _finalize(result)
    return result


def extract_image(path: Path, config: dict) -> ExtractionResult:
    result = ExtractionResult(source_file=path.name, file_type="image")
    result.page_count = 1
    ocr_cfg = (config.get("documents") or {}).get("ocr") or {}
    if ocr_cfg.get("enabled", True) and shutil.which("tesseract"):
        try:
            import pytesseract
            from PIL import Image
            text = pytesseract.image_to_string(Image.open(path)).strip()
            result.pages.append(PageResult(1, "ocr", len(text), text))
        except Exception as exc:  # noqa: BLE001
            result.pages.append(PageResult(1, "image-only", 0, "", needs_vision=True))
            result.warnings.append(f"Local OCR failed ({exc}). Use the local vision model.")
    else:
        result.pages.append(PageResult(1, "image-only", 0, "", needs_vision=True))
        result.warnings.append("OCR unavailable — this image needs the local vision model.")
    _finalize(result)
    return result


def _finalize(result: ExtractionResult) -> None:
    result.full_text = "\n\n".join(p.text for p in result.pages if p.text)
    result.methods_used = sorted({p.method for p in result.pages})
    result.document_type, result.classification_confidence = classify(result.full_text)
    if any(p.needs_vision for p in result.pages):
        result.warnings.append(
            "Some pages produced no text and need the local vision model "
            "(Qwen3-VL). They were NOT sent anywhere."
        )
    total = sum(p.char_count for p in result.pages)
    if total < 50:
        result.warnings.append(
            "Almost no text was extracted. Confirm the file is a real document and "
            "not an empty or corrupt PDF."
        )


EXTRACTORS = {
    ".pdf": extract_pdf, ".docx": extract_docx, ".xlsx": extract_xlsx, ".xlsm": extract_xlsx,
    ".png": extract_image, ".jpg": extract_image, ".jpeg": extract_image,
    ".tif": extract_image, ".tiff": extract_image, ".webp": extract_image,
}


def extract(path: Path) -> ExtractionResult:
    config = load_config()
    suffix = path.suffix.lower()
    handler = EXTRACTORS.get(suffix)
    if not handler:
        raise SystemExit(
            f"Unsupported file type {suffix!r}. Supported: {', '.join(sorted(EXTRACTORS))}"
        )
    if not path.exists():
        raise SystemExit(f"No such file: {path}")
    return handler(path, config)


def to_dict(result: ExtractionResult) -> dict:
    data = asdict(result)
    data["pages"] = [asdict(p) if not isinstance(p, dict) else p for p in result.pages]
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract a document locally.")
    parser.add_argument("file")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--classify-only", action="store_true")
    parser.add_argument("--max-chars", type=int, default=1500)
    args = parser.parse_args()

    result = extract(Path(args.file))

    if args.json:
        print(json.dumps(to_dict(result), indent=2))
        return 0

    print(f"\n  Local extraction — {result.source_file}\n  " + "-" * 50)
    print(f"  File type      : {result.file_type}")
    print(f"  Pages          : {result.page_count}")
    print(f"  Methods used   : {', '.join(result.methods_used) or 'none'}")
    print(f"  Document type  : {result.document_type} (confidence: {result.classification_confidence})")
    print(f"  Tables found   : {len(result.tables)}")
    print(f"  Processed      : entirely on this machine")

    if result.warnings:
        print("\n  Warnings")
        for warning in result.warnings:
            print(f"    - {warning}")

    if not args.classify_only and result.full_text:
        print("\n  Extracted text (first "
              f"{args.max_chars} chars)\n  " + "-" * 50)
        for line in result.full_text[:args.max_chars].splitlines():
            print(f"  {line}")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
