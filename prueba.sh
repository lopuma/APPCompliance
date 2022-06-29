#! /bin/bash


build_prompt(){
	EXIT=$?
	

	if [ $EXIT != 0 ]; then # add arrow color dependent on exit code 
		echo "el valor es <-- : $EXIT"
	else 
		echo "el valor es --> : $EXIT" 
	fi 
}

build_prompt