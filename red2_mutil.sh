#! /bin/bash
# this script will only work if run using the source command (.)
# which will executie the script in the current (bash) shell  
# Source: http://www.paulruffle.com/oracdr.htm

# note: should not need these as they should be in .bashrc 
# export STARLINK_DIR=/hcm/Harry/Radio-Astronomy/Software/star-2015B
# source $STARLINK_DIR/etc/profile
CURRENT_FOLDER="/home/harry/workspace/Python/DataCanadianAstronomy"
MY_PARINI=${CURRENT_FOLDER}/mypar.ini
UTDATE=`date +%Y%m%d`
list_dir=`ls -d */`
for folder in $list_dir
do
	folder=`echo $folder|sed 's|/||g'`
	SLS_DATA_DIR=${CURRENT_FOLDER}/$folder
	# set data in and out paths to match standard jac oracdr pathnames
	UTDATE=`date +%Y%m%d`
	SLS_DATA_IN=${SLS_DATA_DIR}/raw
	SLS_DATA_OUT=${SLS_DATA_DIR}/reduced/acsis/${UTDATE}
	mkdir -p ${SLS_DATA_OUT}
	# test for correct data sub-directory name
	if [ ! -d "$SLS_DATA_DIR" ]; then
	    echo "Error! Data sub-directory $SLS_DATA_DIR does not exist"
	    return
	else
		MY_SERLIST=$SLS_DATA_OUT/ser.list
		/bin/ls -1  $SLS_DATA_DIR/raw/*sdf* > $MY_SERLIST
	fi
	if [ ! -f "$MY_PARINI" ]; then
	    echo "parini file not found!"
	    exit 1
	fi
	echo "PAR: ${MY_PARINI}"
	echo "SERLIST: ${MY_SERLIST}"
	echo "Data in: ${SLS_DATA_IN}"
	echo "Data out: ${SLS_DATA_OUT}"
	echo

	export ORAC_DATA_ROOT=${SLS_DATA_DIR}
	oracdr_acsis ${UTDATE}

	#ORAC_DATA_IN: the location where data are read from. 
	#If running with -loop flag, this is the location of the flag files, rather than the data files.
	export ORAC_NFS_OK=1
	export ORAC_DATA_IN=${SLS_DATA_IN}
	export ORAC_DATA_OUT=${SLS_DATA_OUT}
	# now we can run oracdr

	oracdr -loop file -files $MY_SERLIST REDUCE_SCIENCE_NARROWLINE -recpars $MY_PARINI -nodisplay -log s -batch
	#echo "Delete Raw $MY_SERLIST"
	#rm -rf "$SLS_DATA_DIR/raw/"

	unset ORAC_DATA_IN
	unset ORAC_DATA_OUT
done
