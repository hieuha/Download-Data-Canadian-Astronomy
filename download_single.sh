#!/bin/sh
# Author: HieuHT
# Purpose: Download Multi Threads
dir="$1"
if [ -d "$dir" ]
then
    file_link="$dir/$dir.links"
	if [ -f "$file_link" ]; then
		echo "Downloading for $dir"
		download_command="/usr/bin/wget --content-disposition -P '$dir/raw/' --load-cookies cookies.txt {}"
		# echo $download_command
		cat "$file_link" | /usr/bin/parallel --no-notice --gnu "$download_command" && mail -s "Downloaded $dir" hatrunghieuhpvn@gmail.com
	fi
else
    echo "Error: Directory $dir does not exists."
fi

