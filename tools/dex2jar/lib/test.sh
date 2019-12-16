#!/bin/sh

tmp="."
for k in ./*.jar; do
	echo $k
	#tmp="${tmp}:${k}"
	java -Xms512m -Xmx1024m -classpath "${k}" "com.googlecode.dex2jar.tools.Dex2jarCmd" "$@"
done
echo tmp
