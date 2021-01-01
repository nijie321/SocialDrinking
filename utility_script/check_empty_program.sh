#!/bin/bash

program_file_dir="/home/pi/openbehavior/SocialDrinking/python"

num_empty_files=`ls -l $program_file_dir/*.py | awk '{if($5==0) print($9)}' | wc -l`


if [ $num_empty_files -gt 0 ]
then
	cd /home/pi
	
	rm -rf ./openbehavior
	mkdir openbehavior && cd openbehavior

	redownload_code=`git clone https://github.com/nijie321/SocialDrinking.git`
	while kill -0 $redownload_code ; do
		echo "Program is being downloded. Please Wait....."
		sleep 1
	done
	echo "Finished..."
else
	echo "No empty program file."
fi


