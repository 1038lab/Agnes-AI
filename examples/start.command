#!/bin/bash
cd "$(dirname "$0")"
echo "Starting Agnes Playground..."
kill $(lsof -ti:8888) 2>/dev/null
sleep 0.5
python3 server.py &
SERVER_PID=$!
sleep 1
open http://localhost:8888
echo "Server running at http://localhost:8888"
echo "Press Ctrl+C to stop"
wait $SERVER_PID
