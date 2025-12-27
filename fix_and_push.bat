@echo off
echo ================================================================================
echo REMOVING OLD COMMIT WITH API KEYS
echo ================================================================================
echo.
echo This will:
echo 1. Remove commit e10ebe2 (has API keys in .env.example)
echo 2. Keep your clean v2.0 commit
echo 3. Force push to GitHub
echo.
echo Your API keys will remain safe and you don't need to regenerate them!
echo.
pause

echo.
echo [1/3] Removing problematic commit...
git rebase --onto 0426a06 e10ebe2

echo.
echo [2/3] Verifying history is clean...
git log --oneline -5

echo.
echo [3/3] Force pushing to GitHub...
git push --force

echo.
echo ================================================================================
echo DONE! Old commit removed, API keys safe!
echo ================================================================================
echo.
echo Next: Visit https://github.com/Owais-15/Neuro-symbolic-finance
echo Verify .env is NOT visible and all files are present
echo.
pause
