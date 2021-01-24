from PyQt5 import QtCore

class PageNoInternetConnection(object):
	def __init__(self, ui):
		super(PageNoInternetConnection, self).__init__()
		self.ui = ui
	
	def show(self):
		pageWidget = self.ui.newPageWidget()

		self.ui.insetWindowConstruction(pageWidget)

		self.ui.label(pageWidget, text="No internet connection..", fontSize=18, geometry=(0, 280, 600, 40), 
			align=(QtCore.Qt.AlignCenter), styles=None)
		self.ui.button(pageWidget, text="exit", iconType=self.ui.iconTypes.EXIT, fontSize=12, geometry=(260, 335, 90, 30), action=exit, disabled=False)