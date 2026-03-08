from google import genai
from google.genai import types # is that right?

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself). '.' can be used to access the root directory.",
            ),
        },
    ),
    
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of a specified file located in the working directory, providing the first 10000 characters of the file. Longer files are provided in a truncated form.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
	   "file_path": types.Schema(
		type=types.Type.STRING,
		description="The path to the file to read from."),
        },
	required=["file_path"],
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content to a specified file located in the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
           "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write the contents to."),
	   "content": types.Schema(
		type=types.Type.STRING,
		description="The text content to write. This content will overwrite any existing content if the file already exists."),
        },
	required=["file_path", "content"],
    ),
)


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a specified Python file located in the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
           "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to run. The file must be a Python file, as denoted by .py at the end of the file name."),
           "args": types.Schema(
                type=types.Type.ARRAY,
                description="Arguments to supply to the Python file upon its execution.",
		items=types.Schema(type=types.Type.STRING),
		),
        },
	required=["file_path"],
    ),
    
)



