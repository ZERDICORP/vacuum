class Styles(object):
	def __init__(self):
		self.button_css = """
			QPushButton {
				color: #090909;
				font-weight: 400;
				background: #fff;
				border: 1px solid #090909;
				border-radius: 2px;
			}

			QPushButton:hover {
				background: #090909;
				color: #fff;
			}

			QPushButton:disabled {
				color: #aaa;
				background: #CDCDCD;
				border: 1px solid #CDCDCD;
			}
		"""
		self.title_css = """
			font-weight: 400;
		"""
		self.input_css = """
			color: #090909;
			padding-left: 4px;
			background: #F0F0F0;
			border: none;
			border-radius: 0px;
			border-top-left-radius: 2px;
			border-top-right-radius: 2px;
			border-bottom: 1px solid #555;
		"""
		self.enter_message_css = """
			color: #090909;
			background: #F0F0F0;
			border: none;
			border-radius: 0px;
			border-top-left-radius: 2px;
			border-top-right-radius: 2px;
			border-bottom: 1px solid #555;
		"""
		self.messages_area_css = """
			color: #090909;
			background: #fff;
			padding: 5px;
			border: none;
			border-top: 1px solid #555;
			border-bottom: 1px solid #555;
		"""
		self.main = """
			QLabel {
				color: #090909;
			}

			QMessageBox {
				background-color: #fff;
			}

			QMessageBox QLabel {
				color: #090909;
			}

			QMessageBox QPushButton {
				color: #090909;
				font-size: 12px;
				padding: 6px;
				padding-left: 10px;
				padding-right: 10px;
				margin-right: 4px;
				background: #fff;
				border: 1px solid #090909;
				border-radius: 2px;
			}

			QMessageBox QPushButton:hover {
				color: #090909;
				background: #fff;
				border: 1px solid #090909;
			}
		"""