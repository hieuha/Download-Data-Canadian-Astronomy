#!/bin/sh
# Author: HieuHT
# Purpose: Download Multi Threads

if [ ! -f "/usr/bin/parallel" ]; then
	echo "Parallel not found!"
	echo "You should install parallel!"
	echo "-> sudo apt-get install parallel"
else
	list_dir=`ls -d */` || exit
	for dir in $list_dir
	do
		dir=`echo $dir|sed 's|\/||g'`
		file_link="$dir/$dir.links"
		if [ -f "$file_link" ]; then
			download_command="/usr/bin/wget -P '$dir/' --load-cookies cookies.txt {}"
			cat "$file_link" | /usr/bin/parallel --gnu "$download_command"
		fi
	done
fi
