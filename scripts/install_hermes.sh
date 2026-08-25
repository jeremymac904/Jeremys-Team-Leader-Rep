#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Install a FRESH, ISOLATED Hermes Agent for this repository.
#
# Everything lands inside this repository folder:
#
#   vendor/hermes-agent/   a fresh clone of the official Hermes Agent
#   vendor/hermes-venv/    its own Python virtual environment
#   hermes-home/           this repo's private HERMES_HOME
#
# It does NOT touch:
#   ~/.hermes                any existing Hermes home or profile
#   ~/.local/bin/hermes      any existing `hermes` command
#   any other Hermes install anywhere on your machine
#
# Isolation comes from the HERMES_HOME environment variable, which Hermes
# reads as the single source of truth for its home directory. scripts/hermes.sh
# sets it to this repository's hermes-home/ every time.
#
# Usage:
#   bash scripts/install_hermes.sh              install or update
#   bash scripts/install_hermes.sh --check      report status, change nothing
# ---------------------------------------------------------------------------
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENDOR="$REPO/vendor"
SRC="$VENDOR/hermes-agent"
VENV="$VENDOR/hermes-venv"
HOME_DIR="$REPO/hermes-home"
UPSTREAM="https://github.com/NousResearch/hermes-agent.git"

say()  { printf '  %s\n' "$*"; }
fail() { printf '\nERROR: %s\n' "$*" >&2; exit 1; }

if [[ "${1:-}" == "--check" ]]; then
  echo "Hermes installation status"
  echo
  [[ -d "$SRC/.git" ]] && say "[OK     ] source   vendor/hermes-agent" || say "[MISSING] source   vendor/hermes-agent"
  [[ -x "$VENV/bin/hermes" ]] && say "[OK     ] command  vendor/hermes-venv/bin/hermes" || say "[MISSING] command  vendor/hermes-venv/bin/hermes"
  [[ -d "$HOME_DIR" ]] && say "[OK     ] home     hermes-home/" || say "[MISSING] home     hermes-home/"
  echo
  say "Isolated from ~/.hermes: yes (HERMES_HOME is set by scripts/hermes.sh)"
  exit 0
fi

echo
echo "  Installing a fresh Hermes Agent inside this repository"
echo "  ------------------------------------------------------"
echo

command -v git >/dev/null 2>&1 || fail "git is required. Install Xcode command line tools: xcode-select --install"

# Hermes requires Python 3.11+.
PY=""
for candidate in python3.13 python3.12 python3.11 python3; do
  if command -v "$candidate" >/dev/null 2>&1; then
    if "$candidate" -c 'import sys; sys.exit(0 if sys.version_info >= (3,11) else 1)' 2>/dev/null; then
      PY="$candidate"; break
    fi
  fi
done
[[ -n "$PY" ]] || fail "Python 3.11 or newer is required. Found none. Install from https://www.python.org/downloads/"
say "using $($PY -V) at $(command -v "$PY")"

mkdir -p "$VENDOR"

# --- 1. Fresh clone (or update an existing one) ----------------------------
if [[ -d "$SRC/.git" ]]; then
  say "updating existing clone in vendor/hermes-agent"
  git -C "$SRC" pull --ff-only
else
  say "cloning $UPSTREAM"
  say "(this is a fresh copy for this repository only)"
  git -C "$VENDOR" clone --depth 1 "$UPSTREAM" hermes-agent
fi

# --- 2. Its own virtual environment ----------------------------------------
if [[ ! -d "$VENV" ]]; then
  say "creating virtual environment in vendor/hermes-venv"
  "$PY" -m venv "$VENV"
fi

say "installing Hermes Agent (this takes a few minutes the first time)"
"$VENV/bin/python" -m pip install --upgrade pip >/dev/null
if ! "$VENV/bin/python" -m pip install -e "$SRC[all]"; then
  say "the [all] extra failed — retrying with the base install"
  "$VENV/bin/python" -m pip install -e "$SRC"
fi

# --- 3. This repository's private HERMES_HOME ------------------------------
mkdir -p "$HOME_DIR/skills"

echo
echo "  Installed."
echo
[[ -x "$VENV/bin/hermes" ]] && say "command: vendor/hermes-venv/bin/hermes" \
  || say "note: no 'hermes' entry point was created — check the install output above"
say "home:    hermes-home/   (isolated; your ~/.hermes is untouched)"
echo
echo "  Next:"
echo "    python3 scripts/sync_agent.py     load the Team Leader agent into it"
echo "    bash scripts/hermes.sh setup      choose your model provider"
echo "    bash scripts/hermes.sh            start talking to it"
echo
