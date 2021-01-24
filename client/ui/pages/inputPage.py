from PyQt5 import QtWidgets, QtCore

class InputPage(object):
	def __init__(self, ui):
		super(InputPage, self).__init__()
		self.ui = ui

	def show(self, pageWidget, lText, iPlaceholder, validate, bText, iconType, bAction):
		self.ui.insetWindowConstruction(pageWidget)

		isValidateError = lambda: validate.name in self.ui.validator.errors

		title = self.ui.label(pageWidget, text=lText, fontSize=30, geometry=(149, 180, 451, 41), align=(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter),
			styles=None)
		title.setStyleSheet(self.ui.title_css)

		def showErrors():
			self.errorTablo.setText("")
			if isValidateError():
				self.errorTablo.setText(self.ui.validator.errors[validate.name])

		def checkValidate(_, isClicked=False):
			self.ui.validator.validate(inputType=validate.type, inputWidget=self.inputLine, 
				rerender=lambda value: self.inputLine.setText(value) or showErrors(), isClicked=isClicked)
			if isClicked and not isValidateError():
				bAction(self.inputLine.text())

		self.inputLine = QtWidgets.QLineEdit(pageWidget)
		self.inputLine.setPlaceholderText(iPlaceholder)
		self.inputLine.setValidator(validate.validator)
		self.inputLine.setFont(self.ui.font(16))
		self.inputLine.setGeometry(QtCore.QRect(149, 230, 221, 31))
		self.inputLine.setStyleSheet(self.ui.input_css)
		self.inputLine.setObjectName(validate.name)
		self.inputLine.setFocus()
		self.inputLine.textChanged.connect(checkValidate)
		self.inputLine.returnPressed.connect(lambda: checkValidate(None, isClicked=True))

		self.errorTablo = self.ui.label(pageWidget, text="", fontSize=10, geometry=(149, 261, 221, 31), 
			align=(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter), styles=""" color: red; """)

		self.ui.button(pageWidget, text=bText, iconType=iconType, fontSize=16, geometry=(380, 230, 120, 31), action=lambda: checkValidate(None, isClicked=True), 
			disabled=isValidateError())