#!/bin/bash

check_python() {
    # Check for Python installation
    if ! command -v python3 &>/dev/null; then
        echo "Python is not installed."
        read -r -p "Do you want to install Python 3.10.12? (y/n): " install_python
        if [[ "$install_python" == "y" ]]; then
            install_python
        else
            echo "Exiting."
            exit 1
        fi
    else
        PYTHON_VERSION=$(python3 --version | grep -oP '\d+\.\d+')
        if (( $(echo "$PYTHON_VERSION < 3.10" | bc -l) )); then
            echo "Python version is less than 3.10."
            read -r -p "Do you want to update to Python 3.10.12? (y/n): " update_python
            if [[ "$update_python" == "y" ]]; then
                install_python
            else
                echo "Exiting."
                exit 1
            fi
        fi
    fi
}

install_python() {
    echo "Installing Python 3.10.12..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt update
        sudo apt install -y python3.10 python3-pip
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install python@3.10
    else
        echo "Unsupported OS for automatic Python installation."
        exit 1
    fi
}

upgrade_pip() {
    # Upgrade pip
    python3 -m pip install --upgrade pip
}

check_mastermind_ai() {
    # Check if mastermind-ai is installed
    if ! pip show mastermind-ai &>/dev/null; then
        echo "mastermind-ai is not installed. Installing..."
        pip install mastermind-ai
    else
        echo "mastermind-ai is already installed."
        if pip list --outdated | grep mastermind-ai &>/dev/null; then
            read -r -p "An update for mastermind-ai is available. Do you want to update it? (y/n): " update_package
            if [[ "$update_package" == "y" ]]; then
                pip install --upgrade mastermind-ai
            fi
        fi
    fi
}

# Main execution
check_python
upgrade_pip  # Call to upgrade pip
check_mastermind_ai  # Call to check mastermind-ai installation

# Clear the screen and run mastermind
clear
mastermind
