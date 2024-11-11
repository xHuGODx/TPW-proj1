#!/bin/bash

# Start a virtual environment
echo "Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Make and apply migrations
echo "Making migrations..."
python3 manage.py makemigrations
echo "Applying migrations..."
python3 manage.py migrate

# Insert data
echo "Inserting data..."
python3 insertData.py

# Run the server
echo "Starting server..."
python3 manage.py runserver
