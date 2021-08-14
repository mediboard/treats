class Pipeline():
	def __init__(self, context):
		self.context = context

	def prep(self):
		raise RuntimeException('Not implemented')

	def run(self):
		raise RuntimeException('Not implemented')