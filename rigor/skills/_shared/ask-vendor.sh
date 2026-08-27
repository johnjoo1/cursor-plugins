#!/usr/bin/env bash
# Optional cross-vendor reviewer for the rigor skills.
#
# Exits 2 when unconfigured, which is the "when present" test the review skills
# perform. A non-zero exit is normal and means: fall back to same-family review
# and state the correlation caveat in the verdict.
#
# Reads the prompt on stdin, writes the completion to stdout.
# Usage:  echo "$PROMPT" | ask-vendor.sh
set -euo pipefail

: "${GEMINI_MODEL:=gemini-2.5-pro}"

if [[ -z "${GEMINI_API_KEY:-}" ]]; then
  echo "ask-vendor: GEMINI_API_KEY unset; no cross-vendor reviewer configured." >&2
  exit 2
fi

prompt=$(cat)
if [[ -z "$prompt" ]]; then
  echo "ask-vendor: empty prompt on stdin." >&2
  exit 3
fi

payload=$(GEMINI_PROMPT="$prompt" python3 -c '
import json, os
print(json.dumps({"contents":[{"parts":[{"text": os.environ["GEMINI_PROMPT"]}]}]}))')

response=$(curl -sS --fail-with-body --max-time 180 \
  -H "Content-Type: application/json" \
  -H "x-goog-api-key: ${GEMINI_API_KEY}" \
  -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_MODEL}:generateContent" \
  -d "$payload") || { echo "ask-vendor: request failed: $response" >&2; exit 4; }

RESP="$response" python3 -c '
import json, os, sys
try:
    d = json.loads(os.environ["RESP"])
    print(d["candidates"][0]["content"]["parts"][0]["text"])
except (KeyError, IndexError, ValueError):
    print("ask-vendor: unexpected response shape:", os.environ["RESP"][:500], file=sys.stderr)
    sys.exit(5)
'
