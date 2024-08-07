#------------------------------------------------------------------------------------------------------------------------------------------------------#
######## Move downloaded files from Downloads to desired directory

import os
import shutil
import re

def move_to_directory(origin, destination):

	# Compile the regex to match the file name pattern
	pattern = re.compile(r"InformeAforosPorHorasCalzadaCarril\d+_\d+_\d+\.xlsx")

	# Iterate over the files in the downloads directory
	for filename in os.listdir(origin):
	    if pattern.match(filename):
	        # Move the file to the destination directory
	        shutil.move(os.path.join(origin, filename), destination)
	return