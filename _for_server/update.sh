#!/bin/bash

# Name of the screen to check for
SCREEN_NAME="Senior_Design"
SCREEN_PID=$(screen -ls | grep "$SCREEN_NAME" | awk '{print $1}' | cut -d '.' -f1)

# Check if the screen is running
if screen -list | grep -q "\.$SCREEN_NAME"; then
  # If the screen is running, close it
  
  echo "PID of $SCREEN_NAME is: $SCREEN_PID"

  # Git pull
  git pull

  # Call a different bash script
  ./start_server.sh

  screen -S $SCREEN_PID -X quit
  

else
  echo "Screen is not running"
fi