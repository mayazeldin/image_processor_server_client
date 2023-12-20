#!/bin/bash
# Check if Python 3 is already installed
if command -v python3 &>/dev/null; then
    echo "Python 3 is already installed."
else
    # Update the package list and install Python 3
    apt-get update
    apt-get install -y python3
    echo "Python 3 has been installed."
fi

# Check if pip3 is installed
if command -v pip3 &>/dev/null; then
    installed_version=$(pip3 --version | awk '{print $2}')
    required_version="3.7.9"
    if [ "$installed_version" == "$required_version" ]; then
        echo "pip3 version $required_version is already installed."
    else
        # Uninstall the existing pip3
        apt-get remove -y python3-pip
        apt-get autoremove -y
        # Install pip3 version 3.7.9
        apt-get install -y python3=3.7.9-1~18.04
        apt-get install -y python3-pip
        echo "pip3 version $required_version has been installed."
    fi
else
    # Install pip3 for Python 3.7.9
    apt-get install -y python3=3.7.9-1~18.04
    apt-get install -y python3-pip
    echo "pip3 version 3.7.9 has been installed."
fi

pip3 install protobuf==3.19.0
pip3 install grpcio==1.42 grpcio-tools==1.42
pip3 install Pillow

# Check if other dependencies are installed
if command -v git &>/dev/null; then
    echo "git is already installed."
else
    # Install git
    apt-get install -y git
    echo "git has been installed."
fi

chmod +x server.sh
chmod +x client.sh

# Check the installed Python version
python3 --version