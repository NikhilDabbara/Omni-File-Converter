@echo off
setlocal enabledelayedexpansion
title OmniConverter Launcher

cls
echo =====================================================================
echo                     OMNICONVERTER LAUNCHER
echo          Universal File Converter with Smart Recommendations
echo =====================================================================
echo.

:: Detect Python executable dynamically across common Windows installations
set "PYTHON_CMD=python"
if exist "%USERPROFILE%\anaconda3\python.exe" (
    set "PYTHON_CMD=%USERPROFILE%\anaconda3\python.exe"
) else if exist "%LOCALAPPDATA%\anaconda3\python.exe" (
    set "PYTHON_CMD=%LOCALAPPDATA%\anaconda3\python.exe"
) else if exist "C:\ProgramData\anaconda3\python.exe" (
    set "PYTHON_CMD=C:\ProgramData\anaconda3\python.exe"
)

:: Quick check for core modules, auto-install missing dependencies if needed
echo Checking environment dependencies...
"%PYTHON_CMD%" -c "import pdf2docx, streamlit, pandas, PIL" >nul 2>&1
if %errorlevel% neq 0 (
    echo [NOTICE] Installing or updating required packages from requirements.txt...
    "%PYTHON_CMD%" -m pip install -r requirements.txt
    echo.
) else (
    echo [OK] All core dependencies verified.
)

echo Using Python: %PYTHON_CMD%
echo.
echo   Please select how you would like to run OmniConverter:
echo.
echo     [1] Launch Web Application (Streamlit in Browser) - Recommended
echo     [2] Launch Desktop Application (CustomTkinter GUI)
echo     [3] Launch via Docker Compose (Isolated Container)
echo     [4] Run Automated Test Suite
echo     [5] Exit
echo.
echo =====================================================================
set /p choice="Enter your choice (1-5) [Default is 1]: "

if "%choice%"=="" set choice=1

if "%choice%"=="1" goto RUN_WEB
if "%choice%"=="2" goto RUN_DESKTOP
if "%choice%"=="3" goto RUN_DOCKER
if "%choice%"=="4" goto RUN_TESTS
if "%choice%"=="5" goto EXIT_SCRIPT

echo Invalid option selected. Launching Web Application by default...
goto RUN_WEB

:RUN_WEB
echo.
echo Starting Web Application...
echo Opening http://localhost:8501 in your default browser...
start "" http://localhost:8501
"%PYTHON_CMD%" -m streamlit run streamlit_app.py --server.port=8501
pause
goto EXIT_SCRIPT

:RUN_DESKTOP
echo.
echo Starting Desktop GUI Application...
"%PYTHON_CMD%" main.py
pause
goto EXIT_SCRIPT

:RUN_DOCKER
echo.
echo Checking for Docker...
where docker >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Docker was not found in your system PATH.
    echo Please ensure Docker Desktop is installed and running, or choose option 1 or 2.
    echo.
    pause
    goto EXIT_SCRIPT
)
echo Building and launching Docker container...
docker compose up --build
pause
goto EXIT_SCRIPT

:RUN_TESTS
echo.
echo Running Automated Test Suite...
"%PYTHON_CMD%" -m unittest tests.test_converters
echo.
pause
goto EXIT_SCRIPT

:EXIT_SCRIPT
echo.
echo Goodbye!
exit /b 0
