#!/bin/bash
DAT=$(date '+%Y-%m-%d - %H:%M')

echo "start:$DAT - $0 " >> /media/bdub/sdb1/Senior_Design/update.log

SCREEN_NAME="Senior_Design"
SCREEN_PID=$(screen -ls | grep "$SCREEN_NAME" | awk '{print $1}' | cut -d '.' -f1)
PYTHON_PATH="/DB_Management/DB_update.py"

echo "git pull - start"
git pull
echo "git pull - done"

echo "Upgrading the DB - start: $PYTHON_PATH"
python3 "$PYTHON_PATH"
echo "Upgrading the DB - done"

echo "checking for server now"
if screen -list | grep -q "\.$SCREEN_NAME";
then
  echo "PID of $SCREEN_NAME is: $SCREEN_PID"

  screen -S "Senior_Design" -dm python3 main.py &
  screen -S $SCREEN_PID -X quit
else
  echo "Server offline, starting"
  screen -S "Senior_Design" -dm python3 main.py &
fi
