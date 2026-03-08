from functions.run_python_file import run_python_file as RPF

result = RPF("calculator", "main.py")
print(result)

result = RPF("calculator", "main.py", ["3 + 5"])
print(result)

result = RPF("calculator", "tests.py")
print(result)

result = RPF("calculator", "../main.py")
print(result)

result = RPF("calculator", "nonexistent.py")
print(result)

result = RPF("calculator", "lorem.txt")
print(result)
