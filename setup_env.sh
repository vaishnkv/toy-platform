#!/bin/bash

# Use Node.js version 16 with nvm
echo "Switching to Node.js version 16..."
nvm use 16

# Install npm packages in the frontend-app directory
echo "Installing npm packages for frontend-app..."
npm install --prefix frontend-app

# Create a Python virtual environment named testenv
echo "Creating a Python virtual environment named 'testenv'..."
python3 -m venv testenv

# Activate the virtual environment
echo "Activating the virtual environment..."
source testenv/bin/activate

# Install all the packages mentioned in the requirements.txt file
echo "Installing Python packages from requirements.txt..."
pip install -r requirements.txt

# Echo that the installation process is complete
echo "Done with installing the necessary packages"
