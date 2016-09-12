#!/bin/sh

URL=${1:-http://catalog.cse.nd.edu:9097/query.text}
curl -s $URL | awk ' /cpus/ {count = count + $2} END {print "Total CPUs: , count}'

curl -s $URL | awk ' /name/ {names[$2]+= 1}
			END {
				for (name in names) {
					count = count + 1
				}
				print "Total Machines:, count
				}'

curl -s $URL | awk ' /type/ {types[$2]++}
			END {
				for (type in types){
					if (n < types[type]) {
						n = types[type]
						m = type
					}
				}

				print "Most prolific type:", m
			}'