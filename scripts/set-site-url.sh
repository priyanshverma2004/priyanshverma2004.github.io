#!/usr/bin/env bash
# Point the site at a new domain. Usage:
#   ./scripts/set-site-url.sh https://priyanshverma.com
set -euo pipefail

if [ $# -ne 1 ]; then
  echo "usage: $0 https://your-domain.com" >&2
  exit 1
fi

NEW="${1%/}"
OLD="https://priyanshverma2004.github.io"

if [ "$NEW" = "$OLD" ]; then
  echo "Already using $OLD"
  exit 0
fi

cd "$(dirname "$0")/.."

FILES=$(grep -rl "$OLD" --include="*.html" --include="*.xml" --include="*.txt" . || true)
if [ -z "$FILES" ]; then
  echo "No references to $OLD found."
  exit 0
fi

for f in $FILES; do
  # macOS sed; on Linux change '' to nothing after -i
  sed -i '' "s|$OLD|$NEW|g" "$f"
  echo "updated $f"
done

echo
echo "Done. Now update the absolutes in sitemap.xml and robots.txt if you use a subpath."
echo "Remember to regenerate the resume PDF (it prints the resume URL):"
echo "  scripts/.venv/bin/python scripts/make-resume-pdf.py"
