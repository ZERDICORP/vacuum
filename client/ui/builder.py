from client.ui.ui import UI # (←) [-ui object-]
from client.ui.icon_types import IconTypes # (←) [-all images path-]
from client.ui.validator import Validator # (←) [-custopn validator-]
# (↓) [-pages-]
from client.ui.pages.pageYourName import PageYourName
from client.ui.pages.pageMenu import PageMenu
from client.ui.pages.pageConnect import PageConnect
from client.ui.pages.pageCreate import PageCreate
from client.ui.pages.pageSetKey import PageSetKey
from client.ui.pages.pageBias import PageBias
from client.ui.pages.pageExitFromBias import PageExitFromBias
from client.ui.pages.pageNoInternetConnection import PageNoInternetConnection
# (↓) [-page builder-]
class Builder(UI):
	def __init__(self, app, client):
		super(Builder, self).__init__()
		self.app = app
		self.client = client # (←) [-client object-]
		self.iconTypes = IconTypes() # (←) [-icon types-]
		self.validator = Validator(self.client) # (←) [-custom validator object-]
		# (↓) [-pages-]
		self.pageYourName = PageYourName(self)
		self.pageMenu = PageMenu(self)
		self.pageConnect = PageConnect(self)
		self.pageCreate = PageCreate(self)
		self.pageSetKey = PageSetKey(self)
		self.pageBias = PageBias(self)
		self.pageExitFromBias = PageExitFromBias(self)
		self.pageNoInternetConnection = PageNoInternetConnection(self)