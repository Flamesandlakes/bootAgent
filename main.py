
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from functions.call_functions import available_functions, call_function
import time

# loading the key
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
	raise RuntimeError("API Key not found.")

# init client
client = genai.Client(api_key = api_key)

# allowing argument to the parsed from the command-line upon running this script
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="Prompt from user")
parser.add_argument("--verbose", action="store_true", help="Give verbose output")
args = parser.parse_args()


def run_agent(client, messages):
	time.sleep( (60/5)+1 ) # artifical delay, in order to not exhaust per-minute rate limit
	
	response = client.models.generate_content(model = "gemini-2.5-flash", 
						contents = messages,
						config = types.GenerateContentConfig(
							tools = [available_functions],  
							system_instruction = system_prompt, temperature = 0)
						)	
	
	# check if request was successful 
	if response.usage_metadata is None:
		raise RuntimeError("No usage metadata found. Likely cause: Failed request from API.")
	
	# if response was successful, store answers for future context
	if candidates := response.candidates:
		for cand in candidates:
			messages.append(cand.content)
	# verbose printout, if verbose
	if args.verbose:
		X = response.usage_metadata.prompt_token_count
		Y = response.usage_metadata.candidates_token_count
		print(f"User prompt: {args.user_prompt}")
		print(f"Prompt tokens: {X}")
		print(f"Response tokens: {Y}")

	####
	if function_calls := response.function_calls:
		function_responses = []
		for function_call in function_calls:
			#print(f"Calling function: {function_call.name}({function_call.args})")
			result = call_function(function_call)
			if not result.parts:
				raise RuntimeError(f"Empty function response for {function_call.name}, err1")
			if result.parts[0].function_response is None:
				raise RuntimeError(f"Empty function response for {function_call.name}, err2")
			if result.parts[0].function_response.response is None:
				raise RuntimeError(f"Empty function response for {function_call.name}, err3")
			
			# after these check, we now add a successful response to a temp storage
			function_responses.append(result.parts[0]) 
			if args.verbose:
				print(f"-> {result.parts[0].function_response.response}")

		messages.append(types.Content(role="user", parts = function_responses))
		
	
	else:
		print(response.text)
		return True # provides a return signal, that breaks the loop
	
		
	
#def main():
#    print("Hello from bootagent!")


if __name__ == "__main__":
	# limit to how many requests/iterations the agent can run in response to a single user prompt 	
	max_iterations_per_user_prompt = 5

	# init messsage outside of main(), such that it does not reset after each loop
	messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
	for _ in range(max_iterations_per_user_prompt):
		try:
			if run_agent(client, messages): # calls the bot to get an answer, returns a signal seperately based on progress
				break
		except RuntimeError as e:
			print(f"An error occured: {e}")
			sys_exit(1)
	else:
		print("Max iterations reached.")
		
		
