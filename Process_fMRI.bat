@echo off
REM ====================================================
REM  Run prep_fMRI.py and merge.py sequentially on Windows
REM ====================================================

REM --- Move to the folder that contains this batch file ---
cd /d "%~dp0"

REM --- Optional: specify exact Python version (uncomment if needed) ---
REM set PYTHON_PATH=C:\Python38\python.exe

echo ============================================
echo Running prep_fMRI.py ...
echo ============================================

python prep_fMRI.py
if errorlevel 1 (
    echo.
    echo [ERROR] prep_fMRI.py failed.
    pause
    exit /b
)

echo ============================================
echo Running merge.py ...
echo ============================================

python merge.py
if errorlevel 1 (
    echo.
    echo [ERROR] merge.py failed.
    pause
    exit /b
)

echo.
echo ============================================
echo All scripts finished successfully.
echo ============================================

pause