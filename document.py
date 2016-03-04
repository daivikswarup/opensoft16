from page import page

class document:
	def __init__(self):
		self.pdf
		self.pageList

	def process(self):
		self.processPages()

	def processPages(self):
		for p in self.pageList:
			p.process()
