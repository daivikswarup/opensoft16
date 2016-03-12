#!/usr/bin/env python
from document import document
import numpy
import subprocess
import re
import cv2
import matplotlib.pyplot as plt

#requires Ghost Script installed in system Which is default in Ubuntu
def process(pdf_path="a.pdf",job_number = 1):	#pdf_path is pdf name in current directory and job_number is for processing multiple pdf files

	#For windows executable gs must be replaced with gswin32c
	Extraction = subprocess.check_output("gs -sDEVICE=jpg -o file-"+ str(job_number) +"-%02d.jpg -r144 " +pdf_path,shell=True);
	num_vector = map(int, re.findall(r'\d+', Extraction));
	pages_processed = num_vector[len(num_vector)-1];
	img_objects = []
	for i in range(0,pages_processed):
		if i<10:
			img_objects.append(cv2.imread("file-"+str(job_number)+"-"+"0"+str(i+1)+".jpg"));
		else:
			img_objects.append(cv2.imread("file-"+str(job_number)+"-"+str(i+1)+".jpg"));
	return img_objects;

def do(addresses):
	# This function process all the pdfs in the docList
	docList=[]
	count = 0
	for address in addresses:
		e = document()
		e.process(address,count)
		docList.append(e)
		count=count+1
	#docList = []
	#docList.append(e)
	
	#for d in docList:
	#	d.process()
	return docList
docs=["/home/aman/Downloads/opensoft16/a.pdf"]
ret=do(docs)
count =0
for doc in ret:
	print 'Doc'
	print count
	count=count+1
	pgcnt=0
	for pg in doc.pageList:
		print 'page'
		print pgcnt
		pgcnt=pgcnt+1
		for gr in pg.graphList:
			print 'graph'
			#plt.subplot(1,1,1),plt.imshow(gr.image)
			#plt.show()
			plt.subplot(len(gr.textBoxImages)+1,1,1),plt.imshow(gr.image)
			cnt=2
			for j in gr.textBoxImages:
				plt.subplot(len(gr.textBoxImages)+1,1,cnt),plt.imshow(j)
				cnt=cnt+1
			plt.show()
