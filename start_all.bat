@echo off
echo ========================================================
echo   Starting Expense Analytics Application (Aryan Kumar)
echo ========================================================
echo.

echo [1/2] Launching Flask Backend API on http://localhost:5000...
start "Expense Analytics - Backend (Flask)" cmd /k "cd /d %~dp0backend && python app.py"

timeout /t 2 >nul

echo [2/2] Launching Vite Frontend on http://localhost:5173...
start "Expense Analytics - Frontend (Vite)" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo Application started successfully!
echo Open your browser at: http://localhost:5173
echo API Health check:     http://localhost:5000/api/health
echo.
pause
