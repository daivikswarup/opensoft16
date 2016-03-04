from document import document

def __main__():
	# This function process all the pdfs in the docList
	e = document()
	docList = []
	docList.append(e)
	
	for d in docList:
		d.process()