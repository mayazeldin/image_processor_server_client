#!/bin/bash

# Change directory to the image_processors folder
cd "$(dirname "$0")/image_processors"

# Execute server.py with the provided arguments
python3 client.py "$@"