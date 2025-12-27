@echo off
echo ========================================================
echo   NEURO-SYMBOLIC THESIS DEPLOYMENT SCRIPT
echo ========================================================
echo.
echo 1. Cleaning project...
echo.

:: Add any cleanup commands here if needed

echo 2. Pushing to GitHub...
echo.
python push_to_github.py

echo.
echo ========================================================
echo   DEPLOYMENT COMPLETE
echo ========================================================
pause
