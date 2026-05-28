#!/bin/bash

# =============================================================================
# Auto-Income AI Agent - One-Click Deployment Script
# =============================================================================
# This script installs dependencies, starts the server, and opens the dashboard
# =============================================================================

echo "🚀 Auto-Income AI Agent - Deployment Script"
echo "=============================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored messages
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check Python version
print_info "Checking Python version..."
python_version=$(python --version 2>&1 | grep -oP '\d\.\d+' | head -1)
if [[ $(echo "$python_version >= 3.8" | bc -l) -eq 1 ]]; then
    print_success "Python $python_version detected"
else
    print_error "Python 3.8+ required. Current: $python_version"
    exit 1
fi

# Install dependencies
print_info "Installing Python dependencies..."
pip install -q fastapi uvicorn jinja2 apscheduler plotly python-dotenv aiohttp httpx ccxt numpy pandas
print_success "Dependencies installed"

# Check if .env exists
if [ ! -f ".env" ]; then
    print_warning ".env file not found. Creating from .env.example..."
    cp .env.example .env
    print_info "Please edit .env and add your API keys before going LIVE"
fi

# Kill any existing server
print_info "Stopping any existing server..."
pkill -f "uvicorn.*web_server" 2>/dev/null || true
pkill -f "python.*web_server" 2>/dev/null || true
sleep 2

# Start the server
print_info "Starting Auto-Income AI Agent server..."
nohup python web_server.py > server.log 2>&1 &
SERVER_PID=$!
print_success "Server started with PID: $SERVER_PID"

# Wait for server to be ready
print_info "Waiting for server to initialize..."
sleep 5

# Check if server is running
if curl -s http://localhost:8000/api/status > /dev/null; then
    print_success "Server is running and responding!"
else
    print_error "Server failed to start. Check server.log for details."
    exit 1
fi

# Get status
status=$(curl -s http://localhost:8000/api/status)
is_running=$(echo $status | grep -o '"is_running":true' || echo '')
test_mode=$(echo $status | grep -o '"test_mode":true' && echo ' (TEST MODE)' || echo ' (LIVE MODE)')

echo ""
echo "=============================================="
echo "🎉 DEPLOYMENT COMPLETE!"
echo "=============================================="
echo ""
echo "📊 Dashboard URL: http://localhost:8000"
echo "📈 API Status: http://localhost:8000/api/status"
echo "🔧 Mode: $test_mode"
echo ""

if [[ -n "$is_running" ]]; then
    echo "✅ Agents are currently RUNNING"
else
    echo "⏹️  Agents are STOPPED - Click 'Start Agents' in dashboard"
fi

echo ""
echo "=============================================="
echo "🌐 TO ACCESS FROM CHROME BROWSER:"
echo "=============================================="
echo ""
echo "Option 1 - Local Access:"
echo "  → Open: http://localhost:8000"
echo ""
echo "Option 2 - Remote Access (ngrok):"
echo "  → Run: ngrok http 8000"
echo "  → Then open the provided https URL"
echo ""
echo "Option 3 - Deploy to Cloud:"
echo "  → See GO_ONLINE.md for Render/Railway/Replit instructions"
echo ""
echo "=============================================="
echo "📋 QUICK COMMANDS:"
echo "=============================================="
echo "  View logs:     tail -f server.log"
echo "  Stop server:   pkill -f web_server"
echo "  Check status:  curl http://localhost:8000/api/status"
echo "  Restart:       ./deploy.sh"
echo ""
echo "=============================================="
echo "⚠️  IMPORTANT:"
echo "=============================================="
echo "  • Currently in TEST MODE (simulated earnings)"
echo "  • To go LIVE: Edit .env and set TEST_MODE=false"
echo "  • Add your API keys for real trading/freelancing"
echo "  • Agent will self-terminate after 7 loss days"
echo ""
print_success "Ready to make money! Open your browser now!"
echo ""

# Auto-open browser (if possible)
if command -v xdg-open &> /dev/null; then
    print_info "Opening dashboard in browser..."
    xdg-open http://localhost:8000
elif command -v open &> /dev/null; then
    print_info "Opening dashboard in browser..."
    open http://localhost:8000
else
    print_info "Please manually open: http://localhost:8000"
fi
