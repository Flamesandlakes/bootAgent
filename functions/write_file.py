import os

def write_file(working_directory, file_path, content):
	try:
		working_abspath = os.path.abspath(working_directory)
		target_file = os.path.normpath(os.path.join(working_abspath, file_path))
		
		valid_file = os.path.commonpath([working_abspath, target_file]) == working_abspath
		if valid_file == False:
			return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
		if os.path.isdir(target_file):
			return f'Error: Cannot write to "{file_path}" as it is a directory'
		
		# Create any missing parent directories, such that the file has a valid location if it does not already. 
		# This step will have no effect if they already exist.
		os.makedirs(os.path.dirname(target_file), exist_ok = True)

		with open(target_file, "w") as f:
			f.write(content)
		return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
	except Exception as e:
		return f'Error: {e}'
