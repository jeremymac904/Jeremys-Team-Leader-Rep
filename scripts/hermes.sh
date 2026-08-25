#!/usr/bin/env bash
# NOTE: Team Leaders do NOT need this script. Just run `hermes` from this folder.
# This runs the isolated testing copy installed by install_hermes.sh.

# ---------------------------------------------------------------------------
# Run THIS repository's Hermes Agent.
#
# Sets HERMES_HOME to this repository's hermes-home/ so the agent reads this
# repo's config, SOUL, and skills — and never your global ~/.hermes or any
# other Hermes profile on this machine.
#
#   bash scripts/hermes.sh              start a conversation
#   bash scripts/hermes.sh setup        first-time provider/model setup
#   bash scripts/hermes.sh <anything>   any other hermes subcommand
# ---------------------------------------------------------------------------
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BIN="$REPO/vendor/hermes-venv/bin/hermes"

if [[ ! -x "$BIN" ]]; then
  cat >&2 <<MSG

Hermes is not installed in this repository yet.

  bash scripts/install_hermes.sh

That pulls a fresh copy into vendor/ and leaves any other Hermes install on
your machine completely alone.

MSG
  exit 1
fi

# The isolation boundary. Everything Hermes reads or writes stays in this repo.
export HERMES_HOME="$REPO/hermes-home"

# Run from the repository root so Hermes picks up AGENTS.md as project context.
cd "$REPO"
exec "$BIN" "$@"
