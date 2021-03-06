from document import document
import numpy
import subprocess
import re
import cv2

#requires Ghost Script installed in system Which is default in Ubuntu
def process(pdf_path="a.pdf",job_number = 1):	#pdf_path is pdf name in current directory and job_number is for processing multiple pdf files

	#For windows executable gs must be replaced with gswin32c
	Extraction = subprocess.check_output("gs -sDEVICE=pngalpha -o file-"+ str(job_number) +"-%02d.png -r144 " +pdf_path,shell=True);
	num_vector = map(int, re.findall(r'\d+', Extraction));
	pages_processed = num_vector[len(num_vector)-1];
	img_objects = []
	for i in range(0,pages_processed):
		if i<10:
			img_objects.append(cv2.imread("file-"+str(job_number)+"-"+"0"+str(i+1)+".png"));
		else:
			img_objects.append(cv2.imread("file-"+str(job_number)+"-"+str(i+1)+".png"));
	return img_objects;


def __main__():
	# This function process all the pdfs in the docList
	e = document()
	e.process("a.pdf",0)
	#docList = []
	#docList.append(e)
	

	for d in docList:
		d.process()

	#for d in docList:
	#	d.process()

