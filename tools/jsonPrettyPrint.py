import json

def jpprint(data):
	print(json.dumps(json.loads(f'{data}'.replace("'", "\"")), indent=4, sort_keys=True))