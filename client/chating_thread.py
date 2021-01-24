from PyQt5 import QtCore
import copy, pymongo
from easydict import EasyDict as edict
from modules.types import InvisibleTypes, ActionTypes, ExceptionTypes
from modules.timer import Timer

class ChatingThread(QtCore.QThread):
	# (↓) [-signals-]
	showMessages = QtCore.pyqtSignal(list)
	forcedExit = QtCore.pyqtSignal(str)

	def __init__(self, client, connector, enc):
		super(ChatingThread, self).__init__()
		
		self.client = client
		self.connector = connector
		self.enc = enc

		self.updatePeriod = 30
		self.waitingTimeLimit = self.updatePeriod + 10
	
	def init(self):
		self.localMessages = []
		self.localGhosts = []
		self.alreadySentWhoIsThere = False
		self.lastBannedGhostId = None
		self.lastInvisibleMessageId = None
		self.startingMessagesPoint = 0

		self.initGhostsPresentList()

	def initGhostsPresentList(self):
		self.ghostsPresentList = [{
			"name": self.client.ghostName,
			"id": self.client.ghostId
		}]

	def ghostInGhosts(self, ghostId, ghosts):
		return any([ghost["id"] == ghostId for ghost in ghosts])

	def countingVisibleMessages(self, messages):
		return len([message for message in messages if not message["invisible"]])

	def clientInvisibleMessageHandler(self, message):
		if message.text == InvisibleTypes.WHO_IS_THERE:
			self.connector.manager(actionType=ActionTypes.SEND_MESSAGE, ghostName=self.client.ghostName, ghostId=self.client.ghostId,
				text=InvisibleTypes.I_AM_HERE, invisible=True)
			print("I AM HERE")
			if not self.timer.loop:
				self.timer.start()
				self.startingMessagesPoint = self.countingVisibleMessages(self.biasMessages)
			self.timer.reset()
		else:
			self.connector.manager(actionType=ActionTypes.SEND_MESSAGE, ghostName=self.client.ghostName, ghostId=self.client.ghostId,
				text=InvisibleTypes.I_WENT_OUT, invisible=True)
			print("I WENT OUT")
			return ExceptionTypes.WRONG_BIAS_KEY
		self.lastInvisibleMessageId = message.id
		return 0

	def adminInvisibleMessageHandler(self, message):
		if message.text == InvisibleTypes.I_AM_HERE:
			if not self.ghostInGhosts(message.ghost.id, self.localGhosts):
				self.connector.manager(actionType=ActionTypes.SEND_MESSAGE, ghostName="#bias", ghostId=0, 
					text=f"ghost @{message.ghost.name} connect to bias..", encrypt=False)
				self.localGhosts.append(message.ghost)
			if not self.ghostInGhosts(message.ghost.id, self.ghostsPresentList):
				self.ghostsPresentList.append(message.ghost)
				print(f"CLIENT [{message.ghost.name}] HERE")
		elif message.text == InvisibleTypes.I_JOINED:
			print(f"CLIENT [{message.ghost.name}] JOINED")
		elif message.text == InvisibleTypes.I_WENT_OUT:
			self.connector.manager(actionType=ActionTypes.SEND_MESSAGE, ghostName="#bias", ghostId=0, 
				text=f"ghost @{message.ghost.name} disconnect from bias..", encrypt=False)
			self.ghostsPresentList = [ghost for ghost in self.ghostsPresentList if ghost["id"] != message.ghost.id]
			self.localGhosts = [ghost for ghost in self.localGhosts if ghost["id"] != message.ghost.id]
			print(f"CLIENT [{message.ghost.name}] WENT OUT")
		else:
			if self.lastBannedGhostId != message.ghost.id:
				self.connector.manager(actionType=ActionTypes.SEND_MESSAGE, ghostName="#bias", ghostId=0, 
					text=f"ghost @{message.ghost.name} excluded due to invalid key..", encrypt=False)
				self.ghostsPresentList = [ghost for ghost in self.ghostsPresentList if ghost["id"] != message.ghost.id]
				self.localGhosts = [ghost for ghost in self.localGhosts if ghost["id"] != message.ghost.id]
				print(f"CLIENT [{message.ghost.name}] KICKED")
				self.lastBannedGhostId = message.ghost.id
		if not self.timer.loop:
			self.timer.start()
		self.connector.manager(actionType=ActionTypes.DELETE_MESSAGE, id=message.id)
		return 0

	def addMessage(self, message):
		if all(msg.id != message.id for msg in self.localMessages):
			if message.encrypt:
				message.text = self.enc.decrypt(message.text, self.client.KEY)
			self.localMessages.append(message)
			if message.ghost.id != self.client.ghostId:
				self.client.builder.app.alert(self.client.builder, 0)

	def working(self):
		response = 0

		lastMessagesLength = len(self.localMessages)
		self.bias = self.connector.manager(actionType=ActionTypes.GET_BIAS, biasName=self.client.bias.name)
		self.biasMessages = self.bias.messages
		self.ghosts = self.bias.ghosts

		for i in range(len(self.biasMessages)):
			message = edict(copy.copy(self.biasMessages[i]))
			adminMessage = message.ghost.id == "0"
			if not message.invisible:
				self.addMessage(message)
			elif message.invisible:
				message.text = self.enc.decrypt(message.text, self.client.KEY)
				if not self.client.admin and adminMessage and message.id != self.lastInvisibleMessageId:
					response = self.clientInvisibleMessageHandler(message)
				elif self.client.admin and not adminMessage:
					response = self.adminInvisibleMessageHandler(message)

		if not self.client.admin and not self.startingMessagesPoint:
			return response

		if len(self.localMessages) > lastMessagesLength:
			self.showMessages.emit(self.localMessages[self.startingMessagesPoint:])

		if not self.ghostInGhosts(self.client.ghostId, self.ghosts): #and not self.ghostInGhosts(self.client.ghostId, self.ghostsPresentList):
			response = ExceptionTypes.YOU_WHERE_KICKED

		return response

	def clientTimeHandler(self, iSec):
		if iSec >= self.waitingTimeLimit:
			if self.client.ghostId == self.ghosts[1].id:
				print("I AM A NEW ADMIN")
				self.ghosts[1].id = "0"
				self.client.ghostId = "0"
				self.client.admin = True
				self.connector.manager(actionType=ActionTypes.UPDATE_GHOSTS, ghosts=self.ghosts[1:])
				self.connector.manager(actionType=ActionTypes.SEND_MESSAGE, ghostName="#bias", ghostId=0, 
					text=f"now ghost @{self.client.ghostName} is a new admin..", encrypt=False)
				self.initGhostsPresentList()
			self.timer.reset()

	def adminTimeHandler(self, iSec):
		if not self.alreadySentWhoIsThere:
			self.connector.manager(actionType=ActionTypes.SEND_MESSAGE, ghostName=self.client.ghostName, ghostId=self.client.ghostId, 
				text=InvisibleTypes.WHO_IS_THERE, invisible=True)
			print("WHO IS THERE?")
			self.alreadySentWhoIsThere = True

		if iSec >= self.updatePeriod:
			self.connector.manager(actionType=ActionTypes.UPDATE_GHOSTS, ghosts=self.ghostsPresentList)
			print(f"GHOSTS: {str([ghost['name'] for ghost in self.ghostsPresentList])}")
			self.connector.manager(actionType=ActionTypes.UPDATE_MESSAGES, newMessages=[])
			print("DELETE MESSAGES")
			self.alreadySentWhoIsThere = False
			self.timer.reset()
			self.initGhostsPresentList()

	def timing(self):
		if self.timer.loop:
			if not self.client.admin:
				self.clientTimeHandler(self.timer.second())
			elif self.client.admin:
				self.adminTimeHandler(self.timer.second())

	def run(self):
		self.init()
		self.timer = Timer(log=True)
		while True:
			if not self.client.isChating:
				break

			# ---------------- trouble list ----------------
			# - Проблемы с работой приложения в присутсивии более 2 юзеров в биасе.
			# ----------------------------------------------

			try:
				exception = self.working()
				if exception:
					self.forcedExit.emit(exception)
					break
				self.timing()
			except pymongo.errors.ConnectionFailure:
				self.forcedExit.emit(ExceptionTypes.NO_INTERNET_CONNECTION)
				break
			except AttributeError:
				if not self.client.admin:
					self.forcedExit.emit(ExceptionTypes.BIAS_HAS_BEEN_DESTROYED)
				break
		self.timer.stop()
		return