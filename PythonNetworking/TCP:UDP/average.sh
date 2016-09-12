#/bin/sh

awk 'BEGIN{sum = 0;} {++array[$1];} END{for(i in array){ sum += i*array[i]; } avg = sum/10; print (avg);}'