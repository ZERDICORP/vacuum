from sys import argv
from jsonPrettyPrint import jpprint
from easydict import EasyDict as edict
import pymongo
from enc import ENC
from bson.objectid import ObjectId

# create encryptor
enc = ENC(separator=edict({
	"dot": "]",
	"dot_sep": "[",
	"global_sep": "|"
}))

try:
	mongoClient = pymongo.MongoClient(
		"mongodb+srv://admin1:authp4assadmin1@enc01.jp9b3.mongodb.net/vacuum?retryWrites=true&w=majority",
		serverSelectionTimeoutMS=1
	)
	db = mongoClient.vacuum
except:
	mongoClient = None

def showBias(bias):
	newDict = {
		"name": bias["name"],
		"admin": bias["admin"],
		"ghosts": [{**ghost, "id": "..."} for ghost in bias["ghosts"]],
		"messages": [{**message, "ghost": {**message["ghost"], "id": "..."}, "id": "...", "text": (enc.decrypt(message["text"], int(argv[3])) if message["encrypt"] else message["text"]).replace('"', "^"), "encrypt": str(message["encrypt"]), "invisible": str(message["invisible"])} for message in bias["messages"]]
	}
	jpprint(newDict)

def deleteBias(bias):
	db.biases.delete_one({"_id": ObjectId(bias["_id"])})
	print(f"[success]: delete bias \"{argv[2]}\"")

if __name__ == '__main__':
	print("")
	try:
		bias = db.biases.find_one({"name": argv[2]})
		if argv[1] == "-s":
			showBias(bias)
		if argv[1] == "-d":
			deleteBias(bias)
	except TypeError:
		print(f"[error]: no bias with name \"{argv[2]}\"")