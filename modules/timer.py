import threading, time
# (↓) [-TIMER object-]
class Timer(threading.Thread):
	def __init__(self, **kwargs):
		super(Timer, self).__init__(daemon=True)
		self.reseting = kwargs["reseting"] if "reseting" in kwargs else None # (←) [-reset value when self.timer > self.point-]
		self.point = kwargs["point"]  if "point" in kwargs else None # (←) [-time point for reset timer-]
		self.action = kwargs["action"]  if "action" in kwargs else None # (←) [-callback when self.timer > self.point-]
		self.log = kwargs["log"]  if "log" in kwargs else None # (←) [-log timer-]
		self.timer = 0 # (←) [-timer count-]
		self.loop = False # (←) [-is looping-]
	# (↓) [-stop thread loop-]
	def stop(self):
		self.loop = False
	# (↓) [-reset timer-]
	def reset(self):
		self.timer = 0
	# (↓) [-get current second-]
	def second(self):
		return self.timer
	# (↓) [-main loop-]
	def run(self):
		self.loop = True
		# (↓) [-looping if self.loop is True-]
		while self.loop:
			# (↓) [-if is reseting and timer > point-]
			if self.reseting and self.timer > self.point:
				self.reset() # (←) [-reset timer-]
				self.action() # (←) [-call action-]
			# (↓) [-expectation one second-]
			time.sleep(1)
			if self.log:
				print(self.timer)
			# (↓) [-timer increment-]
			self.timer += 1
		return