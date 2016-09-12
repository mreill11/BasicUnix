#!/bin/sh

num=10

while getopts an: option; do
	case $option in
		a) all=1 ;;
		n) num=$OPTARG ;;
		*) echo "usage: $(basename $0) [-a -n N] message"; exit 1 ;;
	esac
done

shift $(($OPTIND - 1))

if [[ $all -eq 1 ]]; then
	du -a -h /etc 2>/dev/null | sort -h -r | head -n $num
else 
	du -h /etc 2>/dev/null | sort -h -r | head -n $num
fi
