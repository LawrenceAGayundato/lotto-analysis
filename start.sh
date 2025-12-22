#!/bin/bash

echo "Starting API server on port 5000..."
python api_server.py &
API_PID=$!

sleep 2

echo "Starting dashboard server on port 8000..."
python serve_dashboard.py &
DASHBOARD_PID=$!

echo ""
echo "Servers running:"
echo "API: http://localhost:5000"
echo "Dashboard: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop"

trap "kill $API_PID $DASHBOARD_PID; exit" INT
wait
