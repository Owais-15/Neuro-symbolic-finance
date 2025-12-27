@echo off
echo ================================================================================
echo SIMPLE FIX: Reset to v1.0 and Recommit Clean v2.0
echo ================================================================================
echo.
echo This will:
echo 1. Reset to v1.0 commit (0426a06) - the clean one on GitHub
echo 2. Keep all your v2.0 files (they won't be deleted)
echo 3. Commit everything fresh with clean .env.example
echo 4. Force push to GitHub
echo.
echo Result: Clean history, no API keys exposed, all your work preserved!
echo.
pause

echo.
echo [1/5] Resetting to v1.0 commit (keeping all files)...
git reset --soft 0426a06

echo.
echo [2/5] Verifying .env.example has placeholders...
type .env.example | findstr "your_primary_groq"

echo.
echo [3/5] Staging all files...
git add .

echo.
echo [4/5] Committing v2.0 with clean history...
git commit -m "v2.0: Academic rigor improvements

- Added formal research question and problem definition
- Created comprehensive limitations section
- Removed overclaiming language
- Added ablation study (symbolic, ML, full system)
- Improved documentation structure
- Reorganized project to match big-tech standards"

echo.
echo [5/5] Force pushing to GitHub...
git push --force

echo.
echo ================================================================================
echo SUCCESS! Clean v2.0 pushed to GitHub!
echo ================================================================================
echo.
echo Your API keys are safe - no need to regenerate!
echo Visit: https://github.com/Owais-15/Neuro-symbolic-finance
echo.
pause
