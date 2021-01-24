from PyQt5 import QtCore, QtWidgets, QtGui

class PageMenu(object):
	def __init__(self, ui):
		super(PageMenu, self).__init__()
		self.ui = ui

	def show(self):
		pageWidget = self.ui.newPageWidget()

		self.ui.insetWindowConstruction(pageWidget) # (←) [-shadow in window bottom-]
		self.ui.nameLabel(pageWidget) # (←) [-user name in top right corner-]

		self.ui.label(pageWidget, text="VACUUM", fontSize=65, geometry=(0, 30, 600, 130), align=(QtCore.Qt.AlignCenter),
			styles=""" font-weight: 300; """)
		self.ui.button(pageWidget, text="Connect to bias", iconType=self.ui.iconTypes.CONNECT, fontSize=18, geometry=(180, 180, 240, 50), 
			action=self.ui.pageConnect.show, disabled=False)
		self.ui.button(pageWidget, text="Create bias", iconType=self.ui.iconTypes.CREATE, fontSize=18, geometry=(180, 250, 240, 50), 
			action=self.ui.pageCreate.show, disabled=False)
		self.ui.button(pageWidget, text="Exit", iconType=self.ui.iconTypes.EXIT, fontSize=18, geometry=(180, 320, 240, 50), 
			action=exit, disabled=False)

		QtWidgets.QShortcut(QtGui.QKeySequence("1"), pageWidget).activated.connect(self.ui.pageConnect.show)
		QtWidgets.QShortcut(QtGui.QKeySequence("2"), pageWidget).activated.connect(self.ui.pageCreate.show)
		QtWidgets.QShortcut(QtGui.QKeySequence("3"), pageWidget).activated.connect(exit)