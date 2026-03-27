#!/bin/bash
# Get the project root directory
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$ROOT_DIR/web/public"
cp "$ROOT_DIR/docs/catalog.json" "$ROOT_DIR/web/public/catalog.json"
echo "✅ catalog.json copied to web/public/"
