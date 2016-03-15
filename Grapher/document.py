from page import page
import numpy
import subprocess
import re
import cv2
import threading
#import pyPdf

class document(threading.Thread):
	def __init__(self,parent,pdf_path,job_number):
		threading.Thread.__init__(self)
		self.parent=parent
		self.pdf=None
		self.pageList=[]
		self.pdf_path = pdf_path
		self.job_number = job_number

	def process(self):
		print self.pdf_path
		Extraction = subprocess.check_output("gs -sDEVICE=jpeg -o  images/file-"+ str(self.job_number) +"-%02d.jpg -r158 " +self.pdf_path,shell=True)
		
		num_vector = map(int, re.findall(r'\d+', Extraction))
		pages_processed = num_vector[len(num_vector)-1]
		print pages_processed
		img_objects = []
		
		for i in range(0,pages_processed):
			if i<10:
				img_objects.append(cv2.imread("images/file-"+str(self.job_number)+"-"+"0"+str(i+1)+".jpg"))
			else:
				img_objects.append(cv2.imread("images/file-"+str(self.job_number)+"-"+str(i+1)+".jpg"))
		#return img_objects;
		
		self.pageList=[]
		pno=0
		for i in img_objects:
			newpage=page(self,pno)
			pno=pno+1
			newpage.pdfImage=i
			self.pageList.append(newpage)

		for p in self.pageList:
			p.start()

		for p in self.pageList:
			p.join()

	def run(self):
		self.process()
		self.parent.RefreshTree()