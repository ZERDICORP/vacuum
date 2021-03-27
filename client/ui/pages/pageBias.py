from PyQt5 import QtWidgets, QtGui, QtCore
from easydict import EasyDict as edict
from client.ui.components.QTextEdit import QTextEdit # (←) [-text edit with modyfied key input function-]

class PageBias(object):
	def __init__(self, ui):
		super(PageBias, self).__init__()
		self.ui = ui
	
	def disconnect(self):
		self.ui.question("You realy want to disconnect? " + 
			(f'\nBias "{self.ui.client.bias.name}" will be deleted..' if self.ui.client.admin else "\nAll messages will disappear.."), 
		action=lambda: self.ui.client.disconnectFromBias() or self.ui.pageMenu.show())

	def rerenderMessages(self, messages):
		newText = ""
		for i in range(len(messages)):
			message = edict(messages[i])
			newText += ("\n" if i > 0 else "") + f"{message.ghost.name}: {message.text}"

		self.viewMessagesArea.setPlainText("")
		self.viewMessagesArea.setPlainText(newText)
		self.viewMessagesArea.moveCursor(QtGui.QTextCursor.End)

	def show(self):
		pageWidget = self.ui.newPageWidget()
		soundIconW, soundIconH = 25, 20
		encryptIconW, encryptIconH = 20, 15
		keyW = QtGui.QFontMetrics(self.ui.font(10)).width(str(self.ui.client.KEY)) + 10
		# (↓) [-send message-]
		def sendMessage():
			value = inputMessage.toPlainText()
			if value:
				self.ui.client.sendGhostMessage(value)
				inputMessage.setPlainText("")
		# (↓) [-label with ghost name-]
		self.ui.label(pageWidget, text=f"@{self.ui.client.ghostName}:", fontSize=16, geometry=(37, 330, 231, 61), 
			align=(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter), styles=None)
		# (↓) [-input messages widget-]
		inputMessage = QTextEdit(pageWidget)
		inputMessage.setEnterAction(enterAction=sendMessage)
		inputMessage.setPlaceholderText("Enter message..")
		inputMessage.setFont(self.ui.font(12))
		inputMessage.setGeometry(QtCore.QRect(278, 330, 231, 61))
		inputMessage.setStyleSheet(self.ui.enter_message_css)
		inputMessage.setFocus(True)
		# (↓) [-send message button-]
		sendButton = self.ui.button(pageWidget, text="send", iconType=self.ui.iconTypes.ZERO, fontSize=16, geometry=(518, 330, 75, 61), action=sendMessage, 
			disabled=False)
		# (↓) [-view messages widget-]
		self.viewMessagesArea = QtWidgets.QPlainTextEdit(pageWidget)
		self.viewMessagesArea.setReadOnly(True)
		self.viewMessagesArea.setFont(self.ui.font(12))
		self.viewMessagesArea.setStyleSheet(self.ui.messages_area_css)
		self.viewMessagesArea.setGeometry(QtCore.QRect(0, 40, 601, 281))
		self.viewMessagesArea.verticalScrollBar().setSingleStep(1)
		# (↓) [-label with bias name-]
		self.ui.label(pageWidget, text=self.ui.client.bias.name, fontSize=16, geometry=(0, 0, 600, 41), align=(QtCore.Qt.AlignCenter), styles=None)
		# (↓) [-icon "lock"-]
		icon = QtWidgets.QLabel(pageWidget)
		icon.setPixmap(self.ui.iconTypes.ENCRYPT.scaled(encryptIconW, encryptIconH))
		icon.setGeometry(QtCore.QRect(600 - encryptIconW - 5, 12, encryptIconW, encryptIconH))
		# (↓) [-secret key-]
		self.ui.label(pageWidget, text=str(self.ui.client.KEY), fontSize=10, geometry=(600 - keyW - encryptIconW, 0, keyW, 40), 
			align=(QtCore.Qt.AlignCenter), styles=None)
		# (↓) [-button "disconnect"-]
		self.ui.button(pageWidget, text="disconnect", iconType=self.ui.iconTypes.DISCONNECT, fontSize=10, geometry=(8, 10, 100, 23), 
			action=self.disconnect, disabled=False)

		QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+B"), pageWidget).activated.connect(self.disconnect)
		QtWidgets.QShortcut(QtGui.QKeySequence("Space"), pageWidget).activated.connect(lambda: inputMessage.setFocus(True))