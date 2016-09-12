#!/bin/sh

#Testing time for all cases

#Testing time to run cgi script
for num in $(seq 50)
do
	./thor.py -a -r 10 http://localhost:9234/cgi-bin/hello.sh >> cgilatency.txt
done

#testing time to display directory
for num in $(seq 50)
do
	./thor.py -a -r 10 http://localhost:9234/ >> dirlatency.txt
done

#testing time to display single file
for num in $(seq 50)
do
	./thor.py -a -r 10 http://localhost:9234/hello.html >> specifiedlatency.txt
done

