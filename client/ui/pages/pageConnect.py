from PyQt5 import QtWidgets, QtGui
from client.ui.pages.inputPage import InputPage
from easydict import EasyDict as edict

class PageConnect(object):
	def __init__(self, ui):
		super(PageConnect, self).__init__()
		self.ui = ui
		self.inputPage = InputPage(self.ui)
	
	def show(self):
		pageWidget = self.ui.newPageWidget()

		self.ui.nameLabel(pageWidget) # (←) [-user name in top right corner-]
		self.ui.cancelButton(pageWidget, self.ui.pageMenu.show) # (←) [-cancel button in top left corner-]
		self.inputPage.show(pageWidget, lText="Connect to bias", iPlaceholder="bias name..", 
			validate=edict({"validator": None, "name": "connectBiasName", "type": "name"}), bText="connect", iconType=self.ui.iconTypes.CONNECT,
			bAction=self.ui.client.connectToBias)

		QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+B"), pageWidget).activated.connect(self.ui.pageMenu.show)