import cv2
import numpy
class document:
	def __init__(self):
		self.pdf
		self.pdfImage
		self.graphList = {}

	def findAllRectangles(self):
		grayScale=cv2.cvtColor(pdfImage,cv2.COLOR_BGR2GRAY)
		edges = cv2.Canny(grayScale,50,150,apertureSize = 3)
		maxlines=100;
		threshhold=1;
		lines = cv2.HoughLines(edges,1,numpy.pi/180,threshhold)
		while(len(lines[0])>maxlines):
			threshhold=threshhold+100
			lines = cv2.HoughLines(edges,1,numpy.pi/180,threshhold)
		verticalLines=[]
		horizontalLines=[]
		delta=0.1
		for rho,theta in lines [0]:
			if(theta<=delta or theta>=numpy.pi-delta):
				# xco-ordinate= rho.cos(theta)  [cos(theta)=plus or munus 1]
				verticalLines.append(rho*numpy.cos(theta));
			if((theta>=numpy.pi/2-delta) and (theta<=numpy.pi/2+delta)):
				horizontalLines.append(rho);
		rectangles=[]
		for iv in range(0,len(verticalLines)):
			for jv in range(iv+1,len(verticalLines)):
				for ih in range(0,len(horizontalLines)):
					for jh in range(ih+1,len(horizontalLines)):\
						rectangles.append(((iv,ih),(jv,jh)))
		return rectangles

	def filterGraphsFromRectangles(self):

	def processGraphs(self):

		for g in self.graphList:
			g.findLabel()
			g.findMarkings()
			g.findColor()
			g.fillData()
