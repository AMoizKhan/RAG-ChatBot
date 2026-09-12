@echo off
echo Starting Backend Server...
start cmd /k "cd /d d:\Raif\backend && python run.py"

echo Starting Frontend Server...
start cmd /k "cd /d d:\Raif\frontend && npm run dev"

echo Both servers are starting!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
