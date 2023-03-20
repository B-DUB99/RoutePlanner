#!/bin/bash

# Name of the screen to check for
SCREEN_NAME="Senior_Design"

# Check if the screen is running
if screen -list | grep -q "\.$SCREEN_NAME"; then
  # If the screen is running, close it
  screen -S $SCREEN_NAME -X quit
  
  # Git pull
  git pull
  
  # Call a different bash script
  ./start_server.sh
else
  echo "Screen is not running"
fi