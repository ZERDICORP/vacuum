from easydict import EasyDict as edict

class Models():
	def __init__(self, enc):
		self.enc = enc

	def bias(self, biasName):
		return {
			"name": biasName,
			"admin": 0,
			"ghosts": [],
			"messages": []
		}

	def ghost(self, ghostName, ghostId):
		return {
			"id": "0" if ghostId == 0 else self.enc.genID(100),
			"name": ghostName 
		}

	def message(self, ghostName, ghostId, text, encrypt, invisible):
		return {
			"ghost": edict({
				"name": ghostName,
				"id": ghostId
			}),
			"id": self.enc.genID(100),
			"text": text,
			"encrypt": encrypt,
			"invisible": invisible
		}