from client.ui.pages.inputPage import InputPage
from easydict import EasyDict as edict

class PageYourName(object):
	def __init__(self, ui):
		super(PageYourName, self).__init__()
		self.ui = ui
		self.inputPage = InputPage(self.ui)

	def show(self):
		pageWidget = self.ui.newPageWidget()

		self.inputPage.show(pageWidget, lText="Your name", iPlaceholder="name..", 
			validate=edict({"validator": None, "name": "yourName", "type": "name"}), bText="start", iconType=self.ui.iconTypes.NEXT, 
			bAction=lambda value: self.ui.client.setGhostName(value) or self.ui.pageMenu.show())
		
