
class document:
	__init__(self):
		self.pdf
		self.pdfImage
		self.graphList = {}

	findAllRectangles(self):

	filterGraphsFromRectangles(self):

	processGraphs(self):

		for g in self.graphList:
			g.findLabel()
			g.findMarkings()
			g.findColor()
			g.fillData()