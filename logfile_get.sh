#This script is used to fetch speed log data from the pi
# "output" folder must exist
# Example ./logfile_get.sh mylogfile.txt
scp pi@192.168.0.31:~/speedy/$1 ./output/$1