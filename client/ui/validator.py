from easydict import EasyDict as edict

class Validator(object):
	def __init__(self, client):
		super(Validator, self).__init__()
		# (↓) [-validate settings-]
		self.client = client
		self.errors = {}
		self.errorTypes = edict({
			"nameMinLen": "minimum length - 2",
			"nameMaxLen": "maximum length - 16",
			"keyEqualZero": "key can not be a zero",
			"keyMinValue": "minimum key value - 1",
			"keyMaxValue": "maximum key value - 1010",
			"biasNotFound": 'bias "{}" not found',
			"biasAlredyExists": 'bias "{}" already exists'
		})
	# (←) [-clear errors dict if no errors-]
	def noErrors(self):
		self.errors = {}
	# (↓) [-set error text-]
	def setError(self, error):
		self.errors[self.objectName]=error
	# (↓) [-validation method-]
	def validate(self, inputType, inputWidget, rerender, isClicked):
		value = inputWidget.text() # (←) [-get text from input widget-]
		self.objectName = inputWidget.objectName()
		# (↓) [-if user enter user or bias name-]
		if inputType == "name":
			# (↓) [-if name length < 2-]
			if len(value) < 2:
				self.setError(f"{self.errorTypes.nameMinLen} (got {len(value)})") # (←) [-add error-]
			# (↓) [-if name length > 16-]
			elif len(value) > 16:
				self.setError(f"{self.errorTypes.nameMaxLen} (got {len(value)})") # (←) [-add error-]
			else:
				if isClicked and self.objectName in ["connectBiasName", "createBiasName"]:
					biases = self.client.getBiases()
					# (↓) [-if this name used in "connect to bias" page-]
					if self.objectName == "connectBiasName":
						# (↓) [-if this bias name not in database-]
						if all(edict(bias).name != value for bias in biases) or not biases:
							self.setError(self.errorTypes.biasNotFound.format(value)) # (←) [-add error-]
						# (↓) [-if this bias name in database-]
						else:
							self.noErrors()
					# (↓) [-if this name used in "create bias" page-]
					elif self.objectName == "createBiasName":
						# (↓) [-if this bias name in database-]
						if biases and any(edict(bias).name == value for bias in biases):
							self.setError(self.errorTypes.biasAlredyExists.format(value)) # (←) [-add error-]
						# (↓) [-if this bias name not in database-]
						else:
							self.noErrors()
					else:
						self.noErrors()
				else:
					self.noErrors()
		# (↓) [-if user enter secret key-]
		elif inputType == "key":
			# (↓) [-if key length equal zero; no key-]
			if len(value) == 0:
				self.setError(self.errorTypes.keyEqualZero) # (←) [-add error-]
			# (↓) [-if key value <= 0-]
			elif int(value) < 1:
				self.setError(self.errorTypes.keyMinValue) # (←) [-add error-]
			# (↓) [-no errors-]
			else:
				self.noErrors()
		# (↓) [-rerender page for show current state-]
		rerender(value)
		