#!/usr/bin/env bash
set -euo pipefail

# ============================================================================
# Deployment Script for Academic Website
# ============================================================================
# This script deploys the generated static site to a web server using rsync.
#
# Usage:
#   ./deploy.sh [options]
#
# Options:
#   --dry-run    Show what would be transferred without actually doing it
#   --verbose    Show detailed transfer information
#   --help       Show this help message
#
# Configuration:
#   Set the following environment variables or edit the defaults below:
#   - DEPLOY_USER: SSH username for the server
#   - DEPLOY_HOST: Server hostname or IP address
#   - DEPLOY_PATH: Remote path where files should be deployed
#   - DEPLOY_PORT: SSH port (default: 22)
# ============================================================================

# Color output for better readability
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

# Show help message
show_help() {
    sed -n '/^# ===/,/^# ===/p' "$0" | sed 's/^# //g' | sed 's/^#//g'
    exit 0
}

# Configuration - Set these values or use environment variables
DEPLOY_USER="${DEPLOY_USER:-}"
DEPLOY_HOST="${DEPLOY_HOST:-}"
DEPLOY_PATH="${DEPLOY_PATH:-}"
DEPLOY_PORT="${DEPLOY_PORT:-22}"

# Script directory and output directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="${SCRIPT_DIR}/output"

# Load configuration from .env file if it exists
ENV_FILE="${SCRIPT_DIR}/.env"
if [[ -f "$ENV_FILE" ]]; then
    log_info "Loading configuration from .env file..."
    # shellcheck disable=SC1090
    source "$ENV_FILE"
else
    log_warning "No .env file found at: $ENV_FILE"
    log_info "You can create one by copying .env.example:"
    log_info "  cp .env.example .env"
fi

# Parse command line arguments
DRY_RUN=""
VERBOSE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN="--dry-run"
            shift
            ;;
        --verbose)
            VERBOSE="--verbose"
            shift
            ;;
        --help|-h)
            show_help
            ;;
        *)
            log_error "Unknown option: $1"
            show_help
            ;;
    esac
done

# ============================================================================
# Validation
# ============================================================================

log_info "Validating deployment configuration..."

# Check if configuration is set
if [[ -z "$DEPLOY_USER" ]] || [[ -z "$DEPLOY_HOST" ]] || [[ -z "$DEPLOY_PATH" ]]; then
    log_error "Deployment configuration is incomplete."
    echo ""
    echo "Please set the following environment variables:"
    echo "  export DEPLOY_USER='your_ssh_username'"
    echo "  export DEPLOY_HOST='your.server.com'"
    echo "  export DEPLOY_PATH='/var/www/html/yoursite'"
    echo ""
    echo "Or edit the defaults in this script (deploy.sh)."
    echo ""
    echo "Optional:"
    echo "  export DEPLOY_PORT='22'  # Default SSH port"
    exit 1
fi

# Check if output directory exists
if [[ ! -d "$OUTPUT_DIR" ]]; then
    log_error "Output directory does not exist: $OUTPUT_DIR"
    log_info "Please run './build.sh' or 'make html' first to generate the site."
    exit 1
fi

# Check if output directory is empty
if [[ -z "$(ls -A "$OUTPUT_DIR")" ]]; then
    log_error "Output directory is empty: $OUTPUT_DIR"
    log_info "Please run './build.sh' or 'make html' first to generate the site."
    exit 1
fi

# Check if rsync is available
if ! command -v rsync &> /dev/null; then
    log_error "rsync is not installed. Please install it first."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "  brew install rsync"
    else
        echo "  sudo apt-get install rsync"
    fi
    exit 1
fi

# Test SSH connection
log_info "Testing SSH connection to ${DEPLOY_USER}@${DEPLOY_HOST}:${DEPLOY_PORT}..."
if ! ssh -p "$DEPLOY_PORT" -o ConnectTimeout=10 -o BatchMode=yes "${DEPLOY_USER}@${DEPLOY_HOST}" exit 2>/dev/null; then
    log_warning "Could not verify SSH connection. Deployment may fail if SSH is not configured."
    log_info "Make sure you have SSH key authentication set up or can authenticate via password."
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "Deployment cancelled."
        exit 0
    fi
fi

# ============================================================================
# Deployment
# ============================================================================

log_info "Deploying to ${DEPLOY_USER}@${DEPLOY_HOST}:${DEPLOY_PATH}"

if [[ -n "$DRY_RUN" ]]; then
    log_warning "Running in DRY-RUN mode - no files will actually be transferred"
fi

# Build rsync command
RSYNC_OPTS=(
    --archive                # Archive mode (recursive, preserve permissions, etc.)
    --compress               # Compress data during transfer
    --delete                 # Delete files on server that don't exist locally
    --exclude='.DS_Store'    # Exclude macOS metadata
    --exclude='*.swp'        # Exclude vim swap files
    --exclude='*~'           # Exclude backup files
)

# Add optional flags
if [[ -n "$VERBOSE" ]]; then
    RSYNC_OPTS+=(--verbose --progress)
fi

if [[ -n "$DRY_RUN" ]]; then
    RSYNC_OPTS+=(--dry-run)
fi

# Add SSH port if not default
if [[ "$DEPLOY_PORT" != "22" ]]; then
    RSYNC_OPTS+=(--rsh="ssh -p ${DEPLOY_PORT}")
else
    RSYNC_OPTS+=(--rsh="ssh")
fi

# Execute rsync
log_info "Starting file transfer..."
if rsync "${RSYNC_OPTS[@]}" "${OUTPUT_DIR}/" "${DEPLOY_USER}@${DEPLOY_HOST}:${DEPLOY_PATH}/"; then
    if [[ -n "$DRY_RUN" ]]; then
        log_success "Dry-run completed. Review the output above to see what would be transferred."
    else
        log_success "Deployment completed successfully!"
        log_info "Your site is now live at: ${DEPLOY_HOST}"
    fi
else
    log_error "Deployment failed. Please check the error messages above."
    exit 1
fi

# ============================================================================
# Post-deployment checks
# ============================================================================

if [[ -z "$DRY_RUN" ]]; then
    log_info "Verifying deployment..."

    # Check if files were actually transferred
    FILE_COUNT=$(ssh -p "$DEPLOY_PORT" "${DEPLOY_USER}@${DEPLOY_HOST}" "find ${DEPLOY_PATH} -type f | wc -l" 2>/dev/null || echo "0")

    if [[ "$FILE_COUNT" -gt 0 ]]; then
        log_success "Verified: ${FILE_COUNT} files found on server"
    else
        log_warning "Could not verify file count on server"
    fi
fi

exit 0
