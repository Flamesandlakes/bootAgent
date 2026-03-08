import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
	try:
		working_abspath  = os.path.abspath(working_directory)
		target_file = os.path.normpath(os.path.join(working_abspath, file_path))
		valid_file = os.path.commonpath([working_abspath, target_file]) == working_abspath
		if valid_file == False:
			return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
		
		if os.path.isfile(target_file) == False:
			return f'Error: "{file_path}" does not exist or is not a regular file'
		if target_file.endswith(".py") == False:
			return f'Error: "{file_path}" is not a Python file'
		
		# constructing command
		command = ["python", target_file]
		if args != None:
			command.extend(args)
		
		# run command
		completed_process = subprocess.run(command, cwd=working_abspath, capture_output = True, text = True, timeout = 30)
		
		# construct output string, based on result of the process
		output = ''

		if returncode := completed_process.returncode: 
			output += f"Process exited with code {returncode}"
		if not completed_process.stdout and not completed_process.stderr:
			output += "No output produced"
		else:
			if stdout := completed_process.stdout:
				output += f"STDOUT:\n{stdout}"
			if stderr := completed_process.stderr:
				output += f"STDERR:\n{stderr}"
		return output
	except Exception as e:
		return f"Error: executing Python file: {e}"
