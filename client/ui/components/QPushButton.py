from PyQt5 import QtWidgets, QtGui, QtCore
# (↓) [-button with custom event filter-]
class QPushButton(QtWidgets.QPushButton):
	def __init__(self, QIcons, isDisabled, centralwidget):
		super(QPushButton, self).__init__(centralwidget)
		self.icon, self.iconHover = QIcons
		self.isDisabled = isDisabled
		
		self.setIcon(QtGui.QIcon(self.icon if not self.isDisabled else self.iconHover))
		self.setDisabled(self.isDisabled)
		self.installEventFilter(self)

	def eventFilter(self, object, event):
		if not self.isDisabled:
			if event.type() == QtCore.QEvent.Enter:
				self.setIcon(QtGui.QIcon(self.iconHover))
				return True
			elif event.type() == QtCore.QEvent.Leave:
				self.setIcon(QtGui.QIcon(self.icon))
				return True
		return False