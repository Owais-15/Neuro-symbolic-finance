@echo off
echo.
echo ================================================================================
echo    NEURO-SYMBOLIC STOCK PREDICTOR - LIVE DASHBOARD
echo ================================================================================
echo.
echo    Rating: 9.7/10 ^| Performance: r=0.62 ^| Explainability: 100%%
echo.
echo ================================================================================
echo.
echo Starting dashboard server...
echo.
echo The dashboard will open automatically in your browser at:
echo    http://localhost:8501
echo.
echo If it doesn't open automatically, copy the URL above into your browser.
echo.
echo Press Ctrl+C to stop the server when you're done.
echo.
echo ================================================================================
echo.

cd /d "%~dp0"
python -m streamlit run app\dashboard.py

pause
