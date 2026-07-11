#!/bin/bash
# Build script for SDI Neural Networks Paper
set -e

PAPER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PAPER_DIR"

echo "=== SDI Paper Build Script ==="
echo "Working directory: $PAPER_DIR"

# Check if pdflatex is available
if ! command -v pdflatex &>/dev/null; then
    echo "pdflatex not found. Installing texlive-full..."
    sudo apt-get update -q
    sudo apt-get install -y texlive-full
fi

echo "--- Step 1: First pdflatex pass ---"
pdflatex -interaction=nonstopmode main.tex

echo "--- Step 2: BibTeX pass ---"
bibtex main

echo "--- Step 3: Second pdflatex pass ---"
pdflatex -interaction=nonstopmode main.tex

echo "--- Step 4: Third pdflatex pass (resolve cross-references) ---"
pdflatex -interaction=nonstopmode main.tex

if [ -f main.pdf ]; then
    echo "=== BUILD SUCCESS ==="
    echo "PDF generated: $PAPER_DIR/main.pdf"
    ls -lh main.pdf
else
    echo "=== BUILD FAILED: main.pdf not found ==="
    exit 1
fi

echo "--- Creating ZIP package ---"
zip -r SDI_paper_v1.zip . \
    --exclude "*.aux" \
    --exclude "*.log" \
    --exclude "*.bbl" \
    --exclude "*.blg" \
    --exclude "*.out" \
    --exclude "*.toc" \
    --exclude "*.fls" \
    --exclude "*.fdb_latexmk" \
    --exclude "__pycache__/*" \
    --exclude "*.pyc"

echo "=== ZIP created: $PAPER_DIR/SDI_paper_v1.zip ==="
ls -lh SDI_paper_v1.zip
