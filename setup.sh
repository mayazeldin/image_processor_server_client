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
    echo "pip3 is already installed."
    # Optionally, you can also check for the specific version here
    PIP_VERSION=$(pip3 --version | awk '{print $2}')
    if [ "$PIP_VERSION" = "3.7.9" ]; then
        echo "pip3 3.7.9 is already installed."
    else
        echo "Upgrading pip3 to version 3.7.9..."
        python3 -m pip install pip==3.7.9
    fi
else
    # Install pip for Python 3
    apt-get install -y python3-pip
    echo "pip3 has been installed."

    # Upgrade to a specific version, if required
    echo "Upgrading pip3 to version 3.7.9..."
    python3 -m pip install pip==3.7.9
fi

pip3 install protobuf==4.21.1
pip3 install grpcio
pip3 install grpcio-tools
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