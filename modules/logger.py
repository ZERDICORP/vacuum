import json

# (↓) [-log request object-]
class LogRequest(object):
	def __init__(self, actType, logType, data):
		self.actType = actType
		self.logType = logType
		self.data = data
# (↓) [-write manager-]
class Writer(object):
	# (↓) [-write log-]
	def write(self, path, data):
		# (↓) [-write to json-]
		with open(path, "w+") as f:
			json.dump(data, f, sort_keys=True, indent=4)
	# (↓) [-add log-]
	def add(self, path, dataToAdd):
		# (↓) [-open and change json content-]
		jsonContent = json.load(open(path)) + [dataToAdd]
		# (↓) [-write result-]
		self.write(path, jsonContent)
	# (↓) [-delete log-]
	def delete(self, path, dataToRemove):
		# (↓) [-open and change json content-]
		jsonContent = [data for data in json.load(open(path)) if data != dataToRemove]
		# (↓) [-write result-]
		self.write(path, jsonContent)
# (↓) [-main logger class-]
class Logger(Writer):
	# (↓) [-write log-]
	def log(self, req):
		if req.actType == "add":
			self.add(req.logType, req.data)
		elif req.actType == "delete":
			self.delete(req.logType, req.data)
	# (↓) [-get log items-]
	def getLog(self, logType):
		return json.load(open(logType))