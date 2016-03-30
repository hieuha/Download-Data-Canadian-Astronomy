# remove special characters in folder name
list_dir=`ls -d */` || exit
for dir in $list_dir
do
	new=`echo -n $dir| sed 's/[^a-zA-Z0-9_]/_/g'`
	mv -f $dir $new
done