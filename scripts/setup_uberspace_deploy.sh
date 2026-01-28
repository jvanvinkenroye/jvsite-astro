#!/bin/bash
#
# Setup Script für Git Hook Deployment auf Uberspace
#
# Ausführen auf Uberspace mit:
#   bash setup_uberspace_deploy.sh
#

set -euo pipefail

echo "🚀 Uberspace Git Hook Deployment Setup"
echo "======================================="
echo ""

# Variablen
REPO_DIR="$HOME/repos"
REPO_NAME="jvsite.git"
WEB_DIR="/var/www/virtual/$USER/html"
BUILD_DIR="$HOME/tmp/jvsite-build"

echo "📁 Verzeichnisse:"
echo "   Bare Repo:    $REPO_DIR/$REPO_NAME"
echo "   Web-Root:     $WEB_DIR"
echo "   Build-Dir:    $BUILD_DIR"
echo ""

# 1. Repos-Verzeichnis erstellen
echo "1️⃣  Erstelle Verzeichnisse..."
mkdir -p "$REPO_DIR"
mkdir -p "$HOME/tmp"

# 2. Bare Repository erstellen
echo "2️⃣  Erstelle Bare Repository..."
if [ -d "$REPO_DIR/$REPO_NAME" ]; then
    echo "   ⚠️  Repository existiert bereits, überspringe..."
else
    git init --bare "$REPO_DIR/$REPO_NAME"
    echo "   ✅ Bare Repository erstellt"
fi

# 3. Post-Receive Hook erstellen
echo "3️⃣  Erstelle Post-Receive Hook..."
cat > "$REPO_DIR/$REPO_NAME/hooks/post-receive" << 'HOOK_EOF'
#!/bin/bash
set -e

# Konfiguration
TARGET="/var/www/virtual/$USER/html"
TEMP_DIR="/home/$USER/tmp/jvsite-build"
REPO_DIR="/home/$USER/repos/jvsite.git"

echo ""
echo "════════════════════════════════════════"
echo "🚀 Deployment gestartet"
echo "════════════════════════════════════════"
echo ""

# Temporäres Verzeichnis vorbereiten
echo "📁 Bereite Build-Verzeichnis vor..."
rm -rf "$TEMP_DIR"
mkdir -p "$TEMP_DIR"

# Code auschecken
echo "📥 Checke Code aus..."
git --work-tree="$TEMP_DIR" --git-dir="$REPO_DIR" checkout -f main

cd "$TEMP_DIR"

# Python Virtual Environment
echo "🐍 Erstelle Python-Umgebung..."
python3 -m venv venv
source venv/bin/activate

echo "📦 Installiere Abhängigkeiten..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Site bauen
echo "🏗️  Baue Webseite mit Pelican..."
pelican content -o output -s pelicanconf.py

# PDFs generieren
echo "📄 Generiere PDFs..."
if [ -f "scripts/generate_teaching_pdf.py" ]; then
    python scripts/generate_teaching_pdf.py || echo "⚠️  Teaching PDF fehlgeschlagen"
fi

# RenderCV falls verfügbar
if command -v rendercv &> /dev/null && [ -f "cv_rendercv.yaml" ]; then
    echo "📄 Generiere CV PDF..."
    rendercv render cv_rendercv.yaml >/dev/null 2>&1 || true
    if [ -f "rendercv_output/Jan_Vanvinkenroye_CV.pdf" ]; then
        mkdir -p output/files
        cp rendercv_output/Jan_Vanvinkenroye_CV.pdf output/files/cv_jan_vanvinkenroye.pdf
    fi
fi

# Zum Webroot deployen
echo "🌐 Kopiere zum Webroot..."
rsync -av --delete "$TEMP_DIR/output/" "$TARGET/"

# Aufräumen
echo "🧹 Räume auf..."
rm -rf "$TEMP_DIR"

echo ""
echo "════════════════════════════════════════"
echo "✅ Deployment erfolgreich!"
echo "🌐 https://$USER.uber.space"
echo "════════════════════════════════════════"
echo ""
HOOK_EOF

chmod +x "$REPO_DIR/$REPO_NAME/hooks/post-receive"
echo "   ✅ Hook erstellt und ausführbar gemacht"

# 4. Zusammenfassung
echo ""
echo "════════════════════════════════════════"
echo "✅ Setup abgeschlossen!"
echo "════════════════════════════════════════"
echo ""
echo "Nächste Schritte auf deinem LOKALEN Rechner:"
echo ""
echo "1. Remote hinzufügen:"
echo "   git remote add uberspace $USER@$(hostname -f):repos/jvsite.git"
echo ""
echo "2. Erstes Deployment:"
echo "   git push uberspace main"
echo ""
echo "3. (Optional) Beide Remotes auf einmal pushen:"
echo "   git remote set-url --add --push origin $USER@$(hostname -f):repos/jvsite.git"
echo "   git push origin main  # pusht zu GitHub UND Uberspace"
echo ""
