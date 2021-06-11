import pymongo
from easydict import EasyDict as edict
# encrypter
from modules.enc import ENC

# connect to mongoDB
try:
	mongoClient = pymongo.MongoClient(
		"mongodb+srv://admin1:OtSvYgxGXiqbwr@enc01.jp9b3.mongodb.net/vacuum?retryWrites=true&w=majority",
		serverSelectionTimeoutMS=1
	)
	db = mongoClient.vacuum
except:
	mongoClient = None

# create encryptor
enc = ENC(separator=edict({
	"dot": "]",
	"dot_sep": "[",
	"global_sep": "|"
}))

client, soundPlayer = None, None
