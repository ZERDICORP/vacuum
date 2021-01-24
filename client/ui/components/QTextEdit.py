from PyQt5 import QtWidgets, QtCore
# (↓) [-text edit object for listen enter event-] 
class QTextEdit(QtWidgets.QTextEdit):
	def setEnterAction(self, enterAction):
		self.enterAction = enterAction

	def keyPressEvent(self, event):
		if event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
			self.enterAction()
			return
		super().keyPressEvent(event)