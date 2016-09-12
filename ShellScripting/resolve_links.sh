for file in *
do
	if [ -h "$file" ]; then
		echo "$file"
	fi
done