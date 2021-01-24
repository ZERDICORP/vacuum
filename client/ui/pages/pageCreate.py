from PyQt5 import QtWidgets, QtGui
from client.ui.pages.inputPage import InputPage
from easydict import EasyDict as edict

class PageCreate(object):
	def __init__(self, ui):
		super(PageCreate, self).__init__()
		self.ui = ui
		self.inputPage = InputPage(self.ui)

	def show(self):
		pageWidget = self.ui.newPageWidget()

		self.ui.nameLabel(pageWidget) # (←) [-user name in top right corner-]
		self.ui.cancelButton(pageWidget, self.ui.pageMenu.show) # (←) [-cancel button in top left corner-]
		self.inputPage.show(pageWidget, lText="Create bias", iPlaceholder="bias name..", 
			validate=edict({"validator": None, "name": "createBiasName", "type": "name"}), bText="create", iconType=self.ui.iconTypes.CREATE,
			bAction=self.ui.client.createBias)

		QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+B"), pageWidget).activated.connect(self.ui.pageMenu.show)