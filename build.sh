#!/bin/bash

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
pelican content -o output -s pelicanconf.py

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
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