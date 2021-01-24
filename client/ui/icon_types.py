from PyQt5 import QtGui
# (↓) [-all images types-]
class IconTypes(object):
	def __init__(self):
		self.baseDir = "client/static/assets"
		self.ZERO = ["", ""]
		self.CANCEL = [
			QtGui.QPixmap(f"{self.baseDir}/cancel/cancel.png"),
			QtGui.QPixmap(f"{self.baseDir}/cancel/cancelHover.png")
		]
		self.NEXT = [
			QtGui.QPixmap(f"{self.baseDir}/next/next.png"),
			QtGui.QPixmap(f"{self.baseDir}/next/nextHover.png")
		]
		self.ACCEPT = [
			QtGui.QPixmap(f"{self.baseDir}/accept/accept.png"),
			QtGui.QPixmap(f"{self.baseDir}/accept/acceptHover.png")
		]
		self.CONNECT = [
			QtGui.QPixmap(f"{self.baseDir}/connect/connect.png"),
			QtGui.QPixmap(f"{self.baseDir}/connect/connectHover.png")
		]
		self.DISCONNECT = [
			QtGui.QPixmap(f"{self.baseDir}/disconnect/disconnect.png"),
			QtGui.QPixmap(f"{self.baseDir}/disconnect/disconnectHover.png")
		]
		self.CREATE = [
			QtGui.QPixmap(f"{self.baseDir}/create/create.png"),
			QtGui.QPixmap(f"{self.baseDir}/create/createHover.png")
		]
		self.EXIT = [
			QtGui.QPixmap(f"{self.baseDir}/exit/exit.png"),
			QtGui.QPixmap(f"{self.baseDir}/exit/exitHover.png")
		]
		self.SOUND = [
			QtGui.QPixmap(f"{self.baseDir}/sound/onSound.jpg"),
			QtGui.QPixmap(f"{self.baseDir}/sound/offSound.jpg")
		]
		self.ENCRYPT = QtGui.QPixmap(f"{self.baseDir}/encrypt.png")
		self.INFO = QtGui.QPixmap(f"{self.baseDir}/info.png")