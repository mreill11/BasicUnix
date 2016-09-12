#!/bin/sh

: ${CC:=gcc}
: ${CFLAGS:="-std=gnu99 -Wall"}
: ${SUFFIXES:=.c}

for file in ./*$SUFFIXES; do

	if [ -f $file  ]; then
		$CC -o ${file%.*} $file $CFLAGS

		if [ $VERBOSE  ]; then
			echo $CC -o ${file%.*} $file $CFLAGS
		fi
	else
		echo $CC: error: $SUFFIXES: No such file or directory
		exit 1
	fi
done
