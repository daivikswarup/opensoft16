from page import page
import numpy
import subprocess
import re
import cv2

class document:
	def __init__(self):
		self.pdf=None
		self.pageList=None

	def process(self,pdf_path,job_number):
		Extraction = subprocess.check_output("gs -sDEVICE=pngalpha -o file-"+ str(job_number) +"-%02d.png -r144 " +pdf_path,shell=True);
		num_vector = map(int, re.findall(r'\d+', Extraction));
		pages_processed = num_vector[len(num_vector)-1];
		img_objects = []
		for i in range(0,pages_processed):
			if i<10:
				img_objects.append(cv2.imread("file-"+str(job_number)+"-"+"0"+str(i+1)+".png"));
			else:
				img_objects.append(cv2.imread("file-"+str(job_number)+"-"+str(i+1)+".png"));
		#return img_objects;
		self.pageList=[]
		pno=1
		for i in img_objects:
			newpage=page(self,pno)
			pno=pno+1
			newpage.pdfImage=i
			self.pageList.append(newpage)

		for p in self.pageList:
			p.process()
