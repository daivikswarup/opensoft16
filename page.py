import cv2
import numpy as np
from matplotlib import pyplot as plt
import utils
min_length = 0.1
threshold = 230
delta=10
class Lines:
	def __init__(self):
		self.total_vertical =0
		self.vert_x = []
		self.vert_topy = []
		self.vert_bottomy = []

		self.total_horizontal =0
		self.hor_y = []
		self.hor_leftx = []
		self.hor_rightx = []
	def length(self, type, i):
		if ( type == 'v'):
			return self.vert_bottomy[i] - self.vert_topy[i]
		if (type =='h'):
			return self.hor_rightx[i]- self.hor_leftx[i]


# This class process a single page of the document
class page:
	def __init__(self):
		self.pdfImage
		self.graphList = []

	def process(self):
		self.findAllRectangles()
		self.filterGraphsFromRectangles()
		self.processGraphList()

	def findAllRectangles(self,image):
		#image = cv2.imread(file_name)
		img = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
		cv2.imwrite('mid.jpg',img);
		kernel = np.ones((2,2), np.uint8)
		img = cv2.erode(img, kernel, iterations=1)
	    #ret, img = cv2.threshold(img2gray, 180, 255, cv2.THRESH_BINARY_INV )

		width = np.size(img,1)
		heigth = np.size(img,0)

		#DP matrix 
		vert_dp = np.zeros((heigth,width), dtype=np.uint16)
		hor_dp = np.zeros((heigth,width), dtype=np.uint16)
		lines = Lines();
		for i in range(1,heigth):
			for j in range(1,width):
				if img[i][j] <= threshold :
					vert_dp[i][j] = vert_dp[i-1][j] + 1
					hor_dp[i][j] = hor_dp[i][j-1] + 1

				if img[i][j] > threshold:
					if vert_dp[i-1][j] >= min_length * heigth:
						if not (vert_dp[i-1][j-1] <= vert_dp[i-1][j] +2 and vert_dp[i-1][j-1]>= vert_dp[i-1][j] /2 ):
							
							k = lines.total_vertical
							lines.vert_x.append(j)
							lines.vert_bottomy.append(i-1)
							lines.vert_topy.append(i - vert_dp[i-1][j] )
							lines.total_vertical = lines.total_vertical +1 
							#print 'added vertical line '

					if hor_dp[i][j-1] >= min_length * heigth:
						if not (hor_dp[i-1][j-1] <= hor_dp[i][j-1] +2 and hor_dp[i-1][j-1]>= hor_dp[i][j-1] / 2 ):
							 
							k = lines.total_horizontal
							lines.hor_y.append(i)
							lines.hor_rightx.append(j-1)
							lines.hor_leftx.append(j- hor_dp[i][j-1] )	
							lines.total_horizontal = lines.total_horizontal +1

		
		#print lines.total_vertical
		#print lines.total_horizontal	
		# Merge close lines 
		todelete=[]
		for i in range(0,lines.total_vertical):
			for j in range(i+1,lines.total_vertical):
				if((abs(lines.vert_topy[i]-lines.vert_topy[j])<=delta) and (abs(lines.vert_bottomy[i]-lines.vert_bottomy[j])<=delta) and (abs(lines.vert_x[i]-lines.vert_x[j])<=delta)):
					todelete.append(j)
		todelete.sort(reverse=True)
		for i in todelete:
			del lines.vert_x[i]
			del lines.vert_bottomy[i]
			del lines.vert_topy[i]
			lines.total_vertical=lines.total_vertical-1
		todelete=[]
		for i in range(0,lines.total_horizontal):
			for j in range(i+1,lines.total_horizontal):
				if((abs(lines.hor_leftx[i]-lines.hor_leftx[j])<=delta) and (abs(lines.hor_rightx[i]-lines.hor_rightx[j])<=delta) and (abs(lines.hor_y[i]-lines.hor_y[j])<=delta)):
					todelete.append(j)
		todelete.sort(reverse=True)
		for i in todelete:
			del lines.hor_y[i]
			del lines.hor_rightx[i]
			del lines.hor_leftx[i]
			lines.total_horizontal=lines.total_horizontal-1

		
		# find Pairs 
		
			# Check text block inside it 
			
			# check intensity 
			
			# instantiate the graph objects 

		'''
		line_img = np.zeros((heigth,width,3),dtype=np.uint8)
		# for i in range(1,heigth):
		# 	for j in range(1,width):
		# 	line_img[i][j][:] = 255		
		print lines.total_vertical
		print lines.total_horizontal	
		for i in range(0,lines.total_vertical):
			print lines.vert_x[i]
			print lines.vert_topy[i]
			print lines.vert_bottomy[i]
			print '\n'
			for j in range(lines.vert_topy[i],lines.vert_bottomy[i]):
				line_img[j][lines.vert_x[i]][:]=255
		cv2.imwrite('vert.jpg',line_img)
		for i in range(0,lines.total_horizontal):
			print lines.hor_y[i]
			print lines.length('h',i)
			for j in range(lines.hor_leftx[i],lines.hor_rightx[i]):
				line_img[lines.hor_y[i]][j][:]=255
		#cv2.imwrite('final.jpg',line_img)'''
		#return lines
		rectangles=[]
		for i in range(0,lines.total_vertical):
			for j in range(0,lines.total_vertical):
				if(i==j):
					continue
				if(lines.vert_x[j]<lines.vert_x[i]):
					continue
				if((abs(lines.vert_topy[i]-lines.vert_topy[j])<=delta) and (abs(lines.vert_bottomy[i]-lines.vert_bottomy[j])<=delta)):
					for k in range(0,lines.total_horizontal):
						if((abs(lines.hor_y[k]-lines.vert_topy[j])<=delta) and (abs(lines.hor_y[k]-lines.vert_topy[i])<=delta) and (abs(lines.hor_rightx[k]-lines.vert_x[j])<=delta) and (abs(lines.hor_leftx[k]-lines.vert_x[i])<=delta)):
							for l in range(0,lines.total_horizontal):
								if(k==l):
									continue
								if(lines.hor_y[l]<lines.hor_y[k]):
									continue
								if((abs(lines.hor_y[l]-lines.vert_bottomy[j])<=delta) and (abs(lines.hor_y[l]-lines.vert_bottomy[i])<=delta) and (abs(lines.hor_rightx[l]-lines.vert_x[j])<=delta) and (abs(lines.hor_leftx[l]-lines.vert_x[i])<=delta)):
									rectangles.append(((lines.hor_y[k],lines.vert_x[i]),(lines.hor_y[l],lines.vert_x[j])))

		todelete=[]
		for i in rectangles:
			for j in rectangles:
				if(i==j):
					continue
				if(i[0][0]<=j[0][0] and i[0][1]<=j[0][1] and i[1][0]>=j[1][0] and i[1][1]>=j[1][1]):
					todelete.append(j)
		for i in todelete:
			try:
				rectangles.remove(i)
			except ValueError:
				pass

		#print len(rectangles)
		return rectangles

	def filterGraphsFromRectangles(self):
		pass

	def processGraphList(self):

		for g in self.graphList:
			g.findLabel()
			g.findMarkings()
			g.findColor()
			g.fillData()


