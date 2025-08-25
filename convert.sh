#!/bin/bash

# Convert Markdown to HTML with Pandoc
# This script converts README.md to index_from_markdown.html with custom CSS

echo "Converting Markdown to HTML..."

# Install pandoc if not available (macOS)
if ! command -v pandoc &> /dev/null; then
    echo "Pandoc not found. Installing..."
    if command -v brew &> /dev/null; then
        brew install pandoc
    else
        echo "Please install Homebrew first or install pandoc manually"
        exit 1
    fi
fi

# Convert with custom CSS
pandoc README.md \
    -f markdown \
    -t html5 \
    -s \
    --css style.css \
    --metadata title="Jan Vanvinkenroye" \
    --metadata lang="de" \
    --metadata viewport="width=device-width, initial-scale=1.0" \
    -o index_from_markdown.html

echo "✅ Conversion complete! File saved as: index_from_markdown.html"
echo "🌐 Open file:///$(pwd)/index_from_markdown.html to view"