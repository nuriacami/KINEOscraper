#------------------------------------------------------------------------------------------------------------------------------------------------------#
######## Move downloaded files from Downloads to desired directory

import os
import shutil
import re

def move_to_directory(origin, destination):

	# Remove all files from the destination directory
	# for file in os.listdir(destination):
	#     file_path = os.path.join(destination, file)
	#     try:
	#         if os.path.isfile(file_path) or os.path.islink(file_path):
	#             os.unlink(file_path)  # Delete the file or symbolic link
	#         elif os.path.isdir(file_path):
	#             shutil.rmtree(file_path)  # Delete the directory
	#     except Exception as e:
	#         print(f'Error deleting file {file_path}: {e}')


    # Compile the regex patterns
    patterns = [
        re.compile(r"InformeAforosPorHorasCalzadaCarril\d+_\d+_\d+\.xlsx"),
        re.compile(r"VolumneTraficoAgrupado\d+_\d+_\d+\.Xlsx")
    ]
    
    # Iterate over the files in the origin directory
    for filename in os.listdir(origin):
        # Check if the filename matches any of the patterns
        if any(pattern.match(filename) for pattern in patterns):
            # Move the file to the destination directory
            shutil.move(os.path.join(origin, filename), destination)

    return