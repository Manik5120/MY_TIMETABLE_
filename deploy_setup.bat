@echo off
echo ========================================
echo   Django Timetable - Railway Deployment
echo ========================================
echo.

echo Step 1: Checking if Git is installed...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Git is not installed!
    echo Please download and install Git from: https://git-scm.com/download/win
    echo After installing Git, run this script again.
    pause
    exit /b 1
)

echo Git is installed! ✓
echo.

echo Step 2: Initializing Git repository...
git init
git add .
git commit -m "Initial commit - Ready for Railway deployment"

echo.
echo Step 3: Next steps:
echo 1. Create a GitHub repository at: https://github.com/new
echo 2. Copy the repository URL
echo 3. Run: git remote add origin YOUR_GITHUB_REPO_URL
echo 4. Run: git push -u origin main
echo 5. Go to railway.app and deploy from your GitHub repo
echo.

echo ========================================
echo   Deployment files are ready! 🚀
echo ========================================
pause
