#!/bin/sh

while getopts d:W name
do
	case $name in
		d)dopt=$OPTARG;;
		W)Wopt=1;;
		*)echo "Invalid argument";;
	esac
done

function remove {
	if [ "$dopt" = "//" ]; then
		sed -e 's/\/\/.*//g'
	else
		sed -e 's/\#.*//g'
	fi
}

shift $(($OPTIND -1))

if [[ ! -z $dopt ]]; then

	if [[ ! -z $Wopt ]]; then

		cat $1 | remove | sed -e 's/[ /t]*$//'

	else

		cat $1 | remove | sed '/^[[:space:]]*$/d' | sed -e 's/[ \t]*$//'

	fi

else

	if [[ ! -z $Wopt ]]; then

		cat $1 | sed -e 's/\#.*//g' | sed -e 's/[ /t]*$//'

	else

		cat $1 | sed -e 's/\#.*//g' | sed '/^[[:space:]]*$/d' | sed -e 's/[ /t]*$//'

	fi

fi

