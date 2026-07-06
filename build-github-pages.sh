#!/usr/bin/env bash
set -euo pipefail

site_dir="_site"

bash ./run-github-pages-hooks.sh

rm -rf "$site_dir"
mkdir -p "$site_dir"

rsync -a ./ "$site_dir"/ \
  --exclude .git/ \
  --exclude .github/ \
  --exclude "$site_dir"/ \
  --exclude .DS_Store \
  --exclude __pycache__/ \
  --exclude .pytest_cache/

uv run python render-readme-index.py README.md "$site_dir/index.html"
uv run python render-readme-index.py HOWTO.md "$site_dir/HOWTO.html"

# Render each project folder's README.md to index.html so bare folder URLs
# resolve on the published site. A folder that ships its own index.html
# (hand-written or via github-pages.sh) keeps it.
for readme in "$site_dir"/*/README.md; do
  [ -f "$readme" ] || continue
  dir="$(dirname "$readme")"
  case "$(basename "$dir")" in _*|.*) continue ;; esac
  if [ ! -f "$dir/index.html" ]; then
    uv run python render-readme-index.py "$readme" "$dir/index.html"
  fi
done

touch "$site_dir/.nojekyll"
