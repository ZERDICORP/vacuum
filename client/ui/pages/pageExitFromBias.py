from PyQt5 import QtCore

class PageExitFromBias(object):
	def __init__(self, ui):
		super(PageExitFromBias, self).__init__()
		self.ui = ui
		
	def show(self, text):
		pageWidget = self.ui.newPageWidget()

		self.ui.insetWindowConstruction(pageWidget)

		self.ui.label(pageWidget, text=text, fontSize=18, geometry=(0, 280, 600, 40), 
			align=(QtCore.Qt.AlignCenter), styles=None)
		self.ui.button(pageWidget, text="menu", iconType=self.ui.iconTypes.DISCONNECT, fontSize=12, geometry=(260, 335, 90, 30),
			action=self.ui.pageMenu.show, disabled=False)