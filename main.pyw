import sys
from PyQt5 import QtWidgets
# (↓) [-models of database objects-]
from models import Models
# (↓) [-connector with mongoDB-]
from connector import Connector
# (↓) [-client logic-]
from client.client import Client
# (↓) [-ui builder-]
from client.ui.builder import Builder
# (↓) [-config-]
from config import *

from modules.types import LogTypes, ActionTypes
from modules.logger import Logger

def checkLog(connector):
	# (↓) [-get forgotten biases-]
	biases = Logger().getLog(LogTypes.FORGOTTEN_BIASES)
	# (↓) [-delete all forgotten biases-]
	for biasId in biases:
		# (↓) [-delete forgotten bias-]
		try:
			connector.manager(actionType=ActionTypes.DELETE_BIAS, biasId=biasId)
		except:
			checkLog(connector)

# (↓) [-start app-]
if __name__ == '__main__':
	if mongoClient:
		models = Models(enc) # (←) [-database object models-]
		connector = Connector(db, models, enc) # (←) [-connector with database-]
		client = Client(connector, enc) # (←) [-client-]
		connector.setClient(client) # (←) [-set client object to connector-]
		#checkLog(connector)
	app = QtWidgets.QApplication(sys.argv) # (←) [-app object-]
	builder = Builder(app, client) # (←) [-initialize ui builder-]
	builder.show() # (←) [-start showing-]
	# (↓) [-if we have internet-]
	if mongoClient:
		client.setBuilder(builder) # (←) [-set builder object to client-]
		builder.pageYourName.show() # (←) [-open page-]
	else:
		builder.pageNoInternetConnection.show() # (←) [-open page-]
	# (↓) [-exit from app-]
	sys.exit(app.exec_())