@echo off
echo ====================================
echo    AQI Shield - GitHub Push Tool
echo ====================================
echo.

cd /d "C:\Users\lenovo\OneDrive\Desktop\AQI"

echo [1/5] Initializing git...
git init

echo [2/5] Setting up git identity...
git config user.email "muakhhir@gmail.com"
git config user.name "AQI Shield"

echo [3/5] Adding all files...
git add .
git status

echo [4/5] Creating first commit...
git commit -m "AQI Shield - AI-powered air quality forecast app"

echo [5/5] Done! Now open browser and:
echo.
echo  1. Go to: https://github.com/new
echo  2. Name it: aqi-shield
echo  3. Keep it PUBLIC, click Create
echo  4. Copy the TWO commands shown (git remote add + git push)
echo  5. Paste them here and press Enter
echo.
cmd /k
