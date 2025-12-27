@echo off
echo ================================================================================
echo QUICK GITHUB PUSH - v2.0 Update
echo ================================================================================
echo.
echo This will commit and push all changes with message:
echo "v2.0: Academic rigor improvements (Tier 1 fixes)"
echo.
echo Press Ctrl+C to cancel, or
pause

echo.
echo [1/4] Staging all files...
git add .

echo.
echo [2/4] Committing...
git commit -m "v2.0: Academic rigor improvements (Tier 1 fixes)

- Added formal research question and problem definition
- Created comprehensive limitations section
- Removed overclaiming language
- Added ablation study (symbolic, ML, full system)
- Improved documentation structure
- Reorganized project to match big-tech standards"

echo.
echo [3/4] Pushing to GitHub...
git push

echo.
echo ================================================================================
echo DONE!
echo ================================================================================
echo.
echo Next steps:
echo 1. Visit your GitHub repository
echo 2. Verify .env is NOT visible
echo 3. Check all files are present
echo.
pause
