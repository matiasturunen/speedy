#!/bin/sh

if [ "$1"=="watch" ]; then
  while inotifywait -qqre modify "."; do
    echo ""
    echo "Copying files..."
      scp -r ./* pi@192.168.0.31:~/speedy/
    echo "Done"
    echo ""
  done
else
  scp -r ./* pi@192.168.0.31:~/speedy/
fi
