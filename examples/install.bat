@echo off
setlocal

:check_python
rem Check for Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed.
    set /p install_python="Do you want to install Python 3.10.12? (y/n): "
    if /i "%install_python%"=="y" (
        call :install_python
    ) else (
        echo Exiting.
        exit /b
    )
) else (
    for /f "tokens=2 delims=." %%a in ('python --version') do (
        if %%a lss 10 (
            echo Python version is less than 3.10.
            set /p update_python="Do you want to update to Python 3.10.12? (y/n): "
            if /i "%update_python%"=="y" (
                call :install_python
            ) else (
                echo Exiting.
                exit /b
            )
        ) else (
            call :upgrade_pip
        )
    )
)

:install_python
echo Installing Python 3.10.12 using winget...
start /wait winget install Python.Python.3.10 --silent
goto :upgrade_pip

:upgrade_pip
rem Upgrade pip
python -m pip install --upgrade pip
goto :check_mastermind_ai

:check_mastermind_ai
rem Check if mastermind-ai is installed
pip show mastermind-ai >nul 2>&1
if %errorlevel% neq 0 (
    echo mastermind-ai is not installed. Installing...
    pip install mastermind-ai
) else (
    echo mastermind-ai is already installed.
    python -m pip list --outdated | findstr mastermind-ai >nul
    if %errorlevel% == 0 (
        set /p update_package="An update for mastermind-ai is available. Do you want to update it? (y/n): "
        if /i "%update_package%"=="y" (
            pip install --upgrade mastermind-ai
        )
    )
)

rem Clear the screen and run mastermind
cls
mastermind
endlocal
