#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Start development server with auto-reload
echo "🚀 Starting Pelican development server..."
echo "📂 Site will be available at: http://localhost:8000"
echo "🔄 Auto-reload enabled - changes will rebuild automatically"
echo ""
echo "Press Ctrl+C to stop the server"

pelican --autoreload --listen