#!/bin/sh

lower=abcdefjhijklmnopqrstuvwxyzabcdefjhijklmnopqrstuvwxyz
upper=ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ

if [ $1 ]; then

	rotat=$1%26

else

	rotat=13

fi 

tr ${lower:0:26}$upper:0:26} ${lower:${rotat}:26}${upper:${rotat}:26} 