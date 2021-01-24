from easydict import EasyDict as edict
from client.chating_thread import ChatingThread # (←) [-chating thread for getting new messages-]
from modules.types import InvisibleTypes, ActionTypes, ExceptionTypes
# (↓) [-client object-]
class Client():
	def __init__(self, connector, enc):
		self.connector = connector # (←) [-connector object-]
		self.enc = enc # (←) [-encrypter object-]
		self.ghostName = None
		self.ghostId = None
		self.admin = False
		self.bias = None
		self.KEY = None
		self.isChating = False # (←) [-chating thread switch-]
		self.isForceExit = False # (←) [-force exit switch-]
	# (↓) [-get biases in database-]
	def getBiases(self):
		return self.connector.manager(actionType=ActionTypes.GET_BIASES)
	# (↓) [-set builder object-]
	def setBuilder(self, builder):
		self.builder = builder
	# (↓) [-set ghost name-]
	def setGhostName(self, ghostName):
		self.ghostName = ghostName
	# (↓) [-set key value and start chating-]
	def setKey(self, KEY):
		self.KEY = int(KEY)
		# (↓) [-if ghost is not admin-]
		if not self.admin:
			self.connector.manager(actionType=ActionTypes.SEND_MESSAGE, ghostName=self.ghostName, ghostId=self.ghostId, 
				text=InvisibleTypes.I_JOINED, invisible=True)
		# (↓) [-if ghost is admin-]
		else:
			self.sendInfoMessage(f'Success create bias "{self.bias.name}"..')
		# (↓) [-start chating-]
		self.startChating()
	# (↓) [-create bias-]
	def createBias(self, biasName):
		self.connector.manager(actionType=ActionTypes.CREATE_BIAS, biasName=biasName)
		self.connectToBias(biasName)
	# (↓) [-connect to bias by biasname-]
	def connectToBias(self, biasName):
		# (↓) [-connect to bias and get response-]
		res = self.connector.manager(actionType=ActionTypes.CONNECT_TO_BIAS, biasName=biasName)
		# (↓) [-set current bias and ghost id-]
		self.bias = res.bias
		self.ghostId, self.admin = res.ghostId, res.ghostId == "0"
		self.builder.pageSetKey.show() # (←) [-open page-]
	# (↓) [-disconnect from current bias-]
	def disconnectFromBias(self):
		self.isChating = False
		# (↓) [-if ghost is admin-]
		if self.admin:
			# (↓) [-delete current bias-]
			self.connector.manager(actionType=ActionTypes.DELETE_BIAS, biasId=str(self.bias._id))
		# (↓) [-if ghost not is admin-]
		else:
			# (↓) [-if this is exit by user wish-]
			if not self.isForceExit:
				self.connector.manager(actionType=ActionTypes.SEND_MESSAGE, ghostName=self.ghostName, ghostId=self.ghostId,
					text=InvisibleTypes.I_WENT_OUT, invisible=True)
				# (↓) [-disconnect from current bias-]
				self.connector.manager(actionType=ActionTypes.DISCONNECT, ghostId=self.ghostId)
		# (↓) [-reset client propertyes-]
		self.ghostId, self.admin = None, False
		self.bias, self.KEY = None, None
		self.isForceExit = False
	# (↓) [-send message by user-]
	def sendGhostMessage(self, text):
		self.connector.manager(actionType=ActionTypes.SEND_MESSAGE, ghostName=f"@{self.ghostName}", ghostId=self.ghostId,
			text=text)
  	# (↓) [-send message by bias; info message-]
	def sendInfoMessage(self, text):
		self.connector.manager(actionType=ActionTypes.SEND_MESSAGE, ghostName="#bias", ghostId=0, text=text, encrypt=False)
	# (↓) [-exit by error-]
	def forcedExit(self, exceptionType):
		# (↓) [-if internet connection is shit-]
		if exceptionType == ExceptionTypes.NO_INTERNET_CONNECTION:
			self.isChating = False # (←) [-stop chating-]
			self.builder.pageNoInternetConnection.show() # (←) [-open page-]
		# (↓) [-is bias will be destroy by admin-]
		else:
			self.isForceExit = True
			text = ""
			if exceptionType == ExceptionTypes.BIAS_HAS_BEEN_DESTROYED:
				text = f'Bias "{self.bias.name}" has been destroyed..'
			elif exceptionType == ExceptionTypes.WRONG_BIAS_KEY:
				text = f'Wrong bias key..'
			elif exceptionType == ExceptionTypes.YOU_WHERE_KICKED:
				text = "You where kicked.."
			self.builder.pageExitFromBias.show(text) # (←) [-open page-]
			self.disconnectFromBias() # (←) [-disconnect from bias; just clear all client propertyes, because isForceExit is True-]
	# (↓) [-chating thread-]
	def startChating(self):
		self.isChating = True
		# (↓) [-create thread-]
		self.chatingThread = ChatingThread(self, self.connector, self.enc)
		self.chatingThread.showMessages.connect(lambda messages: self.builder.pageBias.rerenderMessages(messages)) # (←) [-listen event "showMessages"-]
		self.chatingThread.forcedExit.connect(lambda exceptionType: self.forcedExit(exceptionType)) # (←) [-listen force exit event-]
		self.chatingThread.start() # (←) [-start chating thread-]