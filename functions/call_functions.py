
from google.genai import types
import functions.schema_collection as schema

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

import copy

available_functions = types.Tool(
			function_declarations=[schema.schema_get_files_info,
						schema.schema_get_file_content,
						schema.schema_write_file,
						schema.schema_run_python_file,
						]
			)

def call_function(function_call, verbose = False):
	# function_call : a types.FunctionCall object. Should have 
	try:
		if verbose:
			print(f"Calling function: {function_call.name}({function_call.args})")
		else:
			print(f" - Calling function: {function_call.name}")
		
		function_map = {
				"get_files_info": get_files_info,
				"get_file_content": get_file_content,
				"write_file": write_file,
				"run_python_file": run_python_file
				}

		if name := function_call.name:
			function_name = name
		else:
			function_name = ""
		if function_name not in function_map:
			return types.Content(
    						role="tool",
    						parts=[
        					types.Part.from_function_response(
            					name=function_name,
            					response={"error": f"Unknown function: {function_name}"},
        				)
    				],
			)
		args = dict(function_call.args) if function_call.args else {} # make a shallow copy of the args, else init a empty dict
		args["working_directory"] = "./calculator" # setting thw working dir to the custom project folder
		
		function_result = function_map[function_name](**args)
		
		return types.Content(
    					role="tool",
    					parts=[
					        types.Part.from_function_response(
					            name=function_name,
					            response={"result": function_result},
        			)
    			],
		)
	except Exception as e:
		return types.Content(
                                                role="tool",
                                                parts=[
                                                types.Part.from_function_response(
                                                name=function_name,
                                                response={"error": f"{e}"},
                                        )
                                ],
                        )
