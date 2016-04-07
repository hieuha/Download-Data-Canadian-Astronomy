#! /bin/bash
# this script will only work if run using the source command (.)
# which will executie the script in the current (bash) shell  
# Source: http://www.paulruffle.com/oracdr.htm

# note: should not need these as they should be in .bashrc 
# export STARLINK_DIR=/hcm/Harry/Radio-Astronomy/Software/star-2015B
# source $STARLINK_DIR/etc/profile
CURRENT_FOLDER="/home/harry/workspace/Python/DataCanadianAstronomy"
MY_PARINI=${CURRENT_FOLDER}/mypar.ini
list_dir=`ls -d */`
for folder in $list_dir
do
	folder=`echo $folder|sed 's|/||g'`
	SLS_DATA_DIR=${CURRENT_FOLDER}/$folder
	echo $SLS_DATA_DIR

	# set data in and out paths to match standard jac oracdr pathnames
	UTDATE=`date +%Y%m%d`
	export SLS_DATA_IN=${SLS_DATA_DIR}/raw
	export SLS_DATA_OUT=${SLS_DATA_DIR}/reduced/acsis/${UTDATE}
	# test for correct data sub-directory name
	if [ ! -d "$SLS_DATA_DIR" ]; then
	    echo "Error! Data sub-directory $SLS_DATA_DIR does not exist"
	    return
	else
		MY_SERLIST=$SLS_DATA_IN/ser.list
		/bin/ls -1  $SLS_DATA_DIR/raw/*sdf* > $MY_SERLIST
	fi
	if [ ! -f "$MY_PARINI" ]; then
	    echo "parini file not found!"
	    exit 1
	fi
	echo "PAR 			:  ${MY_PARINI}"
	echo "SERLIST       :  ${MY_SERLIST}"
	echo "Data directory:  ${SLS_DATA_DIR}"
	echo "UT date of obs:  ${UTDATE}"
	echo
	 # make a directory for the reduced data (but check first)
	if [ -d ${SLS_DATA_OUT} ]; then
	    if [ -e ${SLS_DATA_OUT}/log.qa ]; then
		 	echo "Warning! ${SLS_DATA_OUT}"
		 	echo "         output directory appears to contain reduced data"
	    else
		 	echo "Warning! ${SLS_DATA_OUT}"
		 	echo "         output data directory already exists"
	    fi
    	echo ""
     	echo -n "Are you sure you want to continue? (y)es "
     	read ans
		if [ "$ans" != "y" ] && [ "$ans" != "Y" ] ; then
	 		echo ""
	 		echo "OK terminating script"
	 		echo ""
	 		return
	    fi
	    echo""
	else
	    mkdir -p ${SLS_DATA_OUT}
	    # echo "Created ${SLS_DATA_OUT}"
	fi
	export ORAC_DATA_ROOT=${SLS_DATA_DIR}
	# call oracdr_acsis which sources oracdr_start.sh for ACSIS instrument
	oracdr_acsis ${UTDATE}
	# reset data in and out paths as oracdr_start.sh sets default paths!

	#ORAC_DATA_IN: the location where data are read from. 
	#If running with -loop flag, this is the location of the flag files, rather than the data files.
	export ORAC_DATA_IN=${SLS_DATA_IN}
	export ORAC_DATA_OUT=${SLS_DATA_OUT}
	export ORAC_NFS_OK=1
	echo ORAC_DATA_IN=$ORAC_DATA_IN
	echo ORAC_DATA_OUT=$ORAC_DATA_OUT

	# now we can run oracdr

	oracdr -loop file -files $MY_SERLIST REDUCE_SCIENCE_NARROWLINE -recpars $MY_PARINI -nodisplay -log s -batch
	echo "Delete Raw $MY_SERLIST"
	rm -rf "$SLS_DATA_DIR/raw/"

	unset ORAC_DATA_IN
	unset ORAC_DATA_OUT
done






