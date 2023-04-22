#!/bin/bash

# Name of the screen session to create
SCREEN_NAME="Senior_Design"

# Command to start the Python script
COMMAND="python3 main.py"

sleep 20

# Create a new screen session with the given name, and start the Python script inside it
screen -dmS $SCREEN_NAME $COMMAND