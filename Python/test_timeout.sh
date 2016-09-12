#!/bin/sh
filename="timeout.py"
###################### CHECK IF EXECUTABLE ########################

if ! [ -x $filename ]; then
echo $filename " not executable!"
exit 1
fi

###################### CHECK IF EXITS WITH SUCCESS ########################
for n in $(seq 4); do
if ! ./timeout.py -t 5 sleep $n ;then
    echo $filename " with success failed!"
    exit 1
fi
done

###################### CHECK IF EXITS WITH FAILURE ########################
for x in $(seq 5 2); do
if ! ./timeout.py -t 1 sleep $x ;then
echo $filename "with failure failed!"
exit 1
fi
done

###################### CHECK SHEBANG ########################
FIRSTLINE=`head -n 1 timeout.py`
VALUE="#!/usr/bin/env python2.7"

if [ "$FIRSTLINE" != "$VALUE" ]; then
echo "shebang test failed"
exit 1
fi

###################### CHECK USAGE ########################

if ! ./timeout.py -h | egrep -i "usage" > /dev/null
then
echo "usage test failed"
exit 1
fi

###################### CHECK STDERR ########################
NUMOFLINES=$(wc -l < "timeout.py")

if ! [ "$NUMOFLINES" -gt 6 ];
then
echo "timeout -v test failed!"
echo "$NUMOFLINES"
exit 1
fi

echo "find test successful!"