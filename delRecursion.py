import os, shutil
from sys import argv as args

count = 0

def delRecursion(dir, name):
	global count
	for item in os.listdir(dir):
		path = f"{dir}\\{item}"
		if item == name:
			shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)
			count += 1
		else:
			if os.path.isdir(path):
				delRecursion(path, name)

if __name__ == "__main__":
	del args[0]
	delRecursion(dir="./", name=args[0])
	print(f"\nSuccess delete {count} objects with name \"{args[0]}\"")