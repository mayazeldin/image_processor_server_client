#!/bin/bash

# Check if Python 3 is already installed
if command -v python3 &>/dev/null; then
    echo "Python 3 is already installed."
else
    # Update the package list and install Python 3
    sudo apt-get update
    sudo apt-get install -y python3
    echo "Python 3 has been installed."
fi


# Check if pip is installed
if command -v pip3 &>/dev/null; then
    echo "pip is already installed."
else
    # Install pip for Python 3
    sudo apt-get install -y python3-pip
    echo "pip has been installed."
fi

# Install required Python packages
pip3 install grpcio grpcio-tools protobuf

# Check if other dependencies are installed
if command -v git &>/dev/null; then
    echo "git is already installed."
else
    # Install git
    sudo apt-get install -y git
    echo "git has been installed."
fi

chmod +x server.sh
chmod +x client.sh



# Check the installed Python version
python3 --version