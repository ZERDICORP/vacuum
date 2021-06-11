from sys import exit
from PyQt5 import QtWidgets, QtGui, QtCore
from client.ui.main import Ui_MainWindow # (←) [-main window-]
from client.ui.styles import Styles # (←) [-styles for components-]
from client.ui.components.QPushButton import QPushButton # (←) [-button with custom event filter-]
from client.ui.icon_types import IconTypes # (←) [-all images path-]
from easydict import EasyDict as edict
# (↓) [-main ui object-]
class UI(QtWidgets.QMainWindow, Styles):
	def __init__(self, parent=None):
		QtWidgets.QWidget.__init__(self, parent)
		# (↓) [-load main ui window-]
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self) # (←) [-load main ui window components-]
		self.setWindowIcon(QtGui.QIcon('client/static/assets/ico.ico')) # (←) [-window icon-]
		self.setStyleSheet(self.main) # (←) [-set window styles-]
		self.pointer = QtGui.QCursor(QtCore.Qt.PointingHandCursor) # (←) [-cursor for buttons-]
		# (↓) [-fonts-]
		self.fonts = edict({
			"RobotoLight": QtGui.QFontDatabase.addApplicationFont("client/static/fonts/Roboto-Light.ttf")
		})

	def exit(self):
		exit()

	def closeEvent(self, event):
		if self.client.bias:
			ifAdmin = f'\nBias "{self.client.bias.name}" will be deleted..' if self.client.admin else "\nAll messages will disappear.."

			answer = QtWidgets.QMessageBox.question(self, 'info', f"Do you realy want to exit? {ifAdmin}", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
			if answer == QtWidgets.QMessageBox.Yes:
				self.client.disconnectFromBias()
				self.exit()
			elif answer == QtWidgets.QMessageBox.No:
				event.ignore()
			elif answer == QtWidgets.QMessageBox.Close:
				event.ignore()
		else:
			self.exit()

	def question(self, text, action):
		answer = QtWidgets.QMessageBox.question(self, 'info', text, QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
		if answer == QtWidgets.QMessageBox.Yes:
			action()
		elif answer == QtWidgets.QMessageBox.No:
			return
		elif answer == QtWidgets.QMessageBox.Close:
			return

	def button(self, pageWidget, text, iconType, fontSize, geometry, action, disabled):
		x, y, w, h = geometry

		button = QPushButton(iconType, disabled, pageWidget)
		button.setText(text)
		button.setFont(self.font(fontSize))
		button.setGeometry(QtCore.QRect(x, y, w, h))
		button.setCursor(self.pointer)
		button.setStyleSheet(self.button_css)
		button.clicked.connect(lambda: action())

		return button

	def label(self, pageWidget, text, fontSize, geometry, align, styles):
		x, y, w, h = geometry

		label = QtWidgets.QLabel(pageWidget)
		label.setText(text)
		label.setGeometry(QtCore.QRect(x, y, w, h))
		label.setFont(self.font(fontSize))
		label.setAlignment(align)
		label.setStyleSheet(styles)

		return label

	def insetWindowConstruction(self, pageWidget):
		self.label(pageWidget, text="", fontSize=12, geometry=(0, 300, 600, 100), align=(QtCore.Qt.AlignRight), 
			styles=""" background: qlineargradient(x1:0 y1:0, x2:0 y2:1, stop:0 #fff, stop:1 #808080) """)

	def cancelButton(self, pageWidget, action):
		self.button(pageWidget, text="", iconType=IconTypes().CANCEL, fontSize=18, geometry=(10, 10, 30, 30), 
			action=lambda: self.validator.noErrors() or action(), disabled=False)

	def nameLabel(self, pageWidget):
		self.label(pageWidget, text=self.client.ghostName, fontSize=12, geometry=(40, 0, 560, 30), 
			align=(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter), styles=""" padding-right: 4px; """)

	def newPageWidget(self):
		widget = QtWidgets.QWidget()
		self.setCentralWidget(widget)

		return widget

	def font(self, size):
		loadedFont = QtGui.QFontDatabase.applicationFontFamilies(self.fonts.RobotoLight)[0]
		font = QtGui.QFont()
		font.setFamily(loadedFont)
		font.setPointSize(size)

		return font