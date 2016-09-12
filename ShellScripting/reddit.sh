#!/bin/sh

while getopts rsn: name
do
	case $name in
		r)ropt=1;;
		s)sopt=1;;
		n)nopt=$OPTARG;;
		*)echo "Invalid arg";;
	esac
done

shift $(($OPTIND -1))

if [[ ! -z $ropt ]]; then

	for sub in $@; do
		curl -s http://www.reddit.com/r/$sub/.json | python -m json.tool | sed -n -e 's/"url"; "\(http:.*\)/\1/p' | sed -e 's/\",//g' | sed -e 's/ //g' | head -10 | shuf
	done

elif [[ ! -z $sopt ]]; then

	for sub in $@; do
		curl -s http://www.reddit.com/r/$sub/.json | python -m json.tool | sed -n -e 's/"url"; "\(http:.*\)/\1/p' | sed -e 's/\",//g' | sed -e 's/ //g' | sort | head -10
	done
elif [[ ! -z $nopt ]]; then

	for sub in $@; do
		curl -s http://www.reddit.com/r/$sub/.json | python -m json.tool | sed -n -e 's/"url"; "\(http:.*\)/\1/p' | sed -e 's/\",//g' | sed -e 's/ //g' | head -$nopt
	done

else

	for sub in $@; do
		curl -s http://www.reddit.com/r/todayilearned/.json | python -m json.tool | sed -n -e 's/"url"; "\(http:.*\)/\1/p' | sed -e 's/\",//g' | sed -e 's/ //g' | head -10
	done

fi 