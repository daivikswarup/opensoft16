#!/usr/bin/env python
from document import document
import numpy
import subprocess
import re
import cv2
import matplotlib.pyplot as plt

class top:
	def __init__(self):
		pass
	def do(self,addresses):
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