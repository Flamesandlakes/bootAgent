import os

def get_files_info(working_directory, directory="."):
	try:
		working_abspath = os.path.abspath(working_directory)
		##if directory not in working_abspath:
		##	return f'Error: directory "{directory}" not in working directory "{working_directory}".'
	
		# make full path by joining together working abs path and directory path together
		target_dir = os.path.normpath(os.path.join(working_abspath, directory))

		# check whether the common (ie. shared) path is the same as the abs path
		# Will be True or False
		valid_target_dir = os.path.commonpath([working_abspath, target_dir]) == working_abspath
	
		if valid_target_dir == False:
			return f'Error: Cannot list "{directory}" as it is outside the permitted working directory' 
			
		if os.path.isdir(target_dir) == False:
			return f'Error: "{target_dir}" is not a directory'
	
		scans = []
		for el in os.listdir(target_dir):
			el_path = os.path.join(target_dir, el)
			info = f"- {el}: file_size={os.path.getsize(el_path)} bytes, is_dir={os.path.isdir(el_path)}"
			scans.append(info)
		return "\n".join(scans)
	except Exception as e:
		return f"Error: {e}"


