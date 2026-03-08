
import os

MAX_CHARS = 10_000 #character limit when reading files

def get_file_content(working_directory, file_path):
	try:
		working_abspath = os.path.abspath(working_directory)
		target_file = os.path.normpath(os.path.join(working_abspath, file_path))
		valid_file = os.path.commonpath([working_abspath, target_file]) == working_abspath
		if valid_file == False:
			return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
		if os.path.isfile(target_file) == False:
			return f'Error: File not found or is not a regular file: "{file_path}"'
		
		with open(target_file, "r") as f:
			file_content = f.read(MAX_CHARS)
			if f.read(1):
				file_content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
		return file_content
	except Exception as e:
		return f"Error: {e}"
