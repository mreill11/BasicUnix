#!/bin/sh

nopt='10'

while getopts hn: input; do 
	case $input in
		h) echo " usage: head.sh
				-n N 	Display the first N lines" ;;
		n) nopt=$OPTARG;;
	esac
done

awk "NR <= $nopt "