from easydict import EasyDict as edict
import pymongo, copy
# (↓) [-object id object for bias ids-]
from bson.objectid import ObjectId
from modules.logger import Logger, LogRequest
from modules.types import ActionTypes, LogTypes, ExceptionTypes

class Connector(object):
	def __init__(self, db, models, enc):
		self.db = db # (←) [-database object-]
		self.models = models # (←) [-database models object-]
		self.enc = enc # (←) [-encrypter object-]
		self.logger = Logger() # (←) [-logger and logger type objects-]
	# (↓) [-set client object-]
	def setClient(self, client):
		self.client = client
	# (↓) [-get all biases-]
	def getBiases(self):
		return list(self.db.biases.find())
	# (↓) [-get bias by name-]
	def getBias(self, biasName):
		bias = self.db.biases.find_one({"name": biasName})
		# (↓) [-if bias is-]
		if bias:
			return edict(bias)
		# (↓) [-if not biases with this name-]
		return False
	# (↓) [-create bias by bias name-]
	def createBias(self, biasName):
		newBias = self.models.bias(biasName) # (←) [-create bias model-]
		self.db.biases.insert_one(newBias) # (←) [-add bias model to database-]
		# (↓) [-add bias id to log file-]
		self.logger.log(
			LogRequest(actType="add", logType=LogTypes.FORGOTTEN_BIASES, data=str(self.getBias(biasName)._id)))
	# (↓) [-delete bias by bias id-]
	def deleteBias(self, biasId):
		self.db.biases.delete_one({"_id": ObjectId(biasId)})
		print(f"delete bias: {biasId}")
		# (↓) [-delete bias id from log file-]
		self.logger.log(
			LogRequest(actType="delete", logType=LogTypes.FORGOTTEN_BIASES, data=biasId))
	# (↓) [-connect to bias by bias name-]
	def connectToBias(self, biasName):
		bias = self.getBias(biasName)
		ghosts = bias.ghosts
		ghost = self.models.ghost(ghostName=self.client.ghostName, ghostId=0 if not len(ghosts) else None)
		ghosts.append(ghost) # (←) [-add ghost id to ghosts array-]
		# (↓) [-update ghosts array database-]
		self.db.biases.update_one({"name": bias.name}, {'$set': {"ghosts": bias.ghosts}})
		# (↓) [-return current bias and ghost id-]
		return edict({
			"bias": bias,
			"ghostId": ghost["id"]
		})
	# (↓) [-disconnect from bias by name-]
	def disconnect(self, ghostId):
		ghosts = [ghost for ghost in self.getBias(self.client.bias.name).ghosts if ghost.id != ghostId]
		# (↓) [-update ghosts array in database-]
		self.db.biases.update_one({"name": self.client.bias.name}, {'$set': {"ghosts": ghosts}})
	# (↓) [-send message-]
	def sendMessage(self, ghostName, ghostId, text, encrypt=True, invisible=False):
		messages = self.getBias(self.client.bias.name).messages # (←) [-get messages array-]
		# (↓) [-if messages must be encrypted; if user message-]
		if encrypt:
			text = self.enc.encrypt(text, self.client.KEY) # (←) [-encrypt message text-]
		# (↓) [-create new message model and add to messages-]
		message = self.models.message(ghostName, ghostId, text, encrypt, invisible)
		messages.append(message)
		self.db.biases.update_one({"name": self.client.bias.name}, {'$set': {"messages": messages}}) # (←) [-update messages array in database-]
		return message
	# (↓) [-delete message in db-]
	def deleteMessage(self, id):
		messages = [message for message in self.getBias(self.client.bias.name).messages if message.id != id]
		self.db.biases.update_one({"name": self.client.bias.name}, {'$set': {"messages": messages}})
	# (↓) [-delete message in db-]
	def updateMessages(self, newMessages):
		self.db.biases.update_one({"name": self.client.bias.name}, {'$set': {"messages": newMessages}})
	# (↓) [-update ghosts array in database-]
	def updateGhosts(self, ghosts):
		self.db.biases.update_one({"name": self.client.bias.name}, {'$set': {"ghosts": ghosts}})
	# (↓) [-events manager-]
	def manager(self, **kwargs):
		response = None
		kwargs = edict(kwargs)
		# (↓) [-do some function by action type-]
		try:
			if kwargs.actionType == ActionTypes.UPDATE_MESSAGES:
				response = self.updateMessages(kwargs.newMessages)
			elif kwargs.actionType == ActionTypes.DELETE_MESSAGE:
				response = self.deleteMessage(kwargs.id)
			elif kwargs.actionType == ActionTypes.SEND_MESSAGE:
				del kwargs["actionType"]
				response = self.sendMessage(**kwargs)
			elif kwargs.actionType == ActionTypes.UPDATE_GHOSTS:
				response = self.updateGhosts(kwargs.ghosts)
			elif kwargs.actionType == ActionTypes.DISCONNECT:
				response = self.disconnect(kwargs.ghostId)
			elif kwargs.actionType == ActionTypes.CONNECT_TO_BIAS:
				response = self.connectToBias(kwargs.biasName)
			elif kwargs.actionType == ActionTypes.DELETE_BIAS:
				response = self.deleteBias(kwargs.biasId)
			elif kwargs.actionType == ActionTypes.CREATE_BIAS:
				response = self.createBias(kwargs.biasName)
			elif kwargs.actionType == ActionTypes.GET_BIAS:
				response = self.getBias(kwargs.biasName)
			elif kwargs.actionType == ActionTypes.GET_BIASES:
				response = self.getBiases()
		except pymongo.errors.ConnectionFailure: # (←) [-internet connection error-]
			self.client.forcedExit(ExceptionTypes.NO_INTERNET_CONNECTION) # (←) [-call force exit in client-]
		# (↓) [-return response-]
		return response