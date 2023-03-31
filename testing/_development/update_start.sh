#!/bin/bash
SCREEN_NAME="Senior_Design"
SCREENNAME="SeniorDesign"
SCREEN_PID=$(screen -ls | grep "$SCREEN_NAME" | awk '{print $1}' | cut -d '.' -f1)
SCREENPID=$(screen -ls | grep "$SCREENNAME" | awk '{print $1}' | cut -d '.' -f1)


echo "git pull"
git pull
echo "git pull done"


echo "starting server now"
if screen -list | grep -q "\.$SCREEN_NAME"; then
  echo "PID of $SCREEN_NAME is: $SCREEN_PID"

  screen -S "SeniorDesign" -dm python3 main.py &
  screen -S $SCREEN_PID -X quit
fi


if screen -list | grep -q "\.$SCREENNAME"; then
  echo "PID of $SCREENNAME is: $SCREENPID"
  
  screen -S "Senior_Design" -dm python3 main.py &
  screen -S $SCREENPID -X quit
fi

echo "Server offline, starting"
screen -S "Senior_Design" -dm python3 main.py &
