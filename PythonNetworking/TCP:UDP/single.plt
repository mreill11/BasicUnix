set terminal png
set grid
set style data histogram
set style fill solid border
set xrange [0:4]
set yrange [0:0.02]
set boxwidth 0.95 relative
plot 'single.txt' \
	with boxes \
	lt rgb "blue" \
	notitle
