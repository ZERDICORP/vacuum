from PyQt5 import QtGui
from easydict import EasyDict as edict
from client.ui.pages.inputPage import InputPage

class PageSetKey(object):
	def __init__(self, ui):
		super(PageSetKey, self).__init__()
		self.ui = ui
		self.inputPage = InputPage(self.ui)

	def show(self):
		pageWidget = self.ui.newPageWidget()

		self.ui.nameLabel(pageWidget)
		self.inputPage.show(pageWidget, lText="Your key", iPlaceholder="key..", 
			validate=edict({"validator": QtGui.QIntValidator(), "name": "yourKey", "type": "key"}), bText="set", iconType=self.ui.iconTypes.ACCEPT,
			bAction=lambda value: self.ui.client.setKey(value) or self.ui.pageBias.show())