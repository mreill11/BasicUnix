#!/bin/bash

FIELDS=$(seq 1 7)

for field in $FIELDS; do
    if ! diff -u <(cut -d : -f $field /etc/passwd) <(./cut.py -d : -f $field /etc/passwd); then
	echo "cut test failed on -f $field /etc/passwd!"
	exit 1
    fi
done
    
for field in $FIELDS; do
    if ! diff -u <(cat /etc/passwd | cut -d : -f $field) <(cat /etc/passwd | ./cut.py -d : -f $field); then
	echo "cut test failed on -f $field implicit stdin!"
	exit 1
    fi
done

for field in $FIELDS; do
    if ! diff -u <(cat /etc/passwd | cut -d : -f $field - ) <(cat /etc/passwd | ./cut.py -d : -f $field -); then
	echo "cut test failed on -f $field explicit stdin!"
	exit 1
    fi
done

if ! diff -u <(cat /etc/passwd | cut -d : -f 1,2,3 -) <(cat /etc/passwd | ./cut.py -d : -f 1,2,3 -); then
    echo "cut test failed on -f 1,2,3 explicit stdin!"
    exit 1
fi

echo "cut test successful!"