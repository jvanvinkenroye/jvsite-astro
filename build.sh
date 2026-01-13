#!/usr/bin/env bash
set -euo pipefail

echo "🔧 Setting up Pelican environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Generate site
echo "🏗️  Building site with Pelican..."
if pelican content -o output -s pelicanconf.py; then
    echo "✅ Build successful!"

    # Generate CV PDF with RenderCV
    echo "📄 Generating CV PDF with RenderCV..."
    if command -v rendercv &> /dev/null; then
        if rendercv render cv_rendercv.yaml >/dev/null 2>&1 && [ -f "rendercv_output/Jan_Vanvinkenroye_CV.pdf" ]; then
            cp rendercv_output/Jan_Vanvinkenroye_CV.pdf output/files/cv_jan_vanvinkenroye.pdf
            rm -rf rendercv_output
            echo "✅ CV PDF generated: output/files/cv_jan_vanvinkenroye.pdf"
        else
            echo "⚠️  Warning: CV PDF generation failed"
        fi
    else
        echo "⚠️  Warning: rendercv not found, skipping PDF generation"
    fi

    # Clean up rendercv_output if it exists (in case of partial builds)
    [ -d "rendercv_output" ] && rm -rf rendercv_output

    # Generate ODF spreadsheet from teaching.md
    echo "📊 Generating teaching assignments ODF spreadsheet..."
    if python scripts/generate_teaching_odf.py; then
        echo "✅ Teaching ODF generated: output/files/lehrauftraege.ods"
    else
        echo "⚠️  Warning: Teaching ODF generation failed"
    fi

    echo "🌐 Site generated in: $(pwd)/output/"
    echo "📂 Open file://$(pwd)/output/index.html to view"

    # Optionally serve the site locally
    if command -v python3 &> /dev/null; then
        echo ""
        echo "🚀 To serve locally, run:"
        echo "   cd output && python3 -m http.server 8000"
        echo "   Then open http://localhost:8000"
    fi
else
    echo "❌ Build failed!"
    exit 1
fi