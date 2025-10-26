#!/bin/bash
# Development helper script

echo "🚀 Starting Skogsstyrelsen API in development mode..."
echo ""
echo "Features enabled:"
echo "  ✓ Auto-reload on code changes"
echo "  ✓ Debug logging"
echo "  ✓ Detailed error messages"
echo ""
echo "API will be available at: http://localhost:8000"
echo "API docs at: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop"
echo ""

DEBUG=true uv run skog-api
