#!/bin/sh

COW=/afs/nd.edu/user15/pbui/pub/bin/cowsay

sass() {
	echo "Do you think you're special? " | $COW
	exit 0
}

taunt() {
	echo "Can't touch this *Song plays* "
	EXIT 0
}

echo "Whatchu need?" | $COW

trap sass SIGHUP
trap taunt SIGINT SIGTERM

for i in {1..10}; do
	sleep 1
done

echo "Think faster, goodbye." | $COW

exit 0
