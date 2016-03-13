#!/usr/bin/env python
import re, collections
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

'''
IMPORT spell class 
s = spell(pdf_path)
print s.correct(word to be corrected)
'''
class spell:
  def __init__(self,path):
    self.path = 'a.pdf'
    self.NWORDS = self.convert_pdf_to_txt(self.path)
    self.alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'
  def train(self, features):
      model = collections.defaultdict(lambda: 1)
      #print model
      for f in features:
          model[f] += 1
      return model

  def convert_pdf_to_txt(self,path):
      rsrcmgr = PDFResourceManager()
      retstr = StringIO()
      codec = 'utf-8'
      laparams = LAParams()
      device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
      fp = file(path, 'rb')
      interpreter = PDFPageInterpreter(rsrcmgr, device)
      password = ""
      maxpages = 0
      caching = True
      pagenos=set()

      for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
          interpreter.process_page(page)

      text = retstr.getvalue()

      fp.close()
      device.close()
      retstr.close()
      return self.train(re.findall('[a-z]+',text.lower()))
      



  def words(self,text): return re.findall('[a-z]+', text.lower()) 

  

  def edits1(self,word):
     splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
     deletes    = [a + b[1:] for a, b in splits if b]
     transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
     replaces   = [a + c + b[1:] for a, b in splits for c in self.alphabet if b]
     inserts    = [a + c + b     for a, b in splits for c in self.alphabet]
     return set(deletes + transposes + replaces + inserts)

  def known_edits2(self,word):
      return set(e2 for e1 in self.edits1(word) for e2 in self.edits1(e1) if e2 in self.NWORDS)

  def known(self,words): return set(w for w in words if w in self.NWORDS)

  def correct(self,word):
      # if not self.NWORDS:
      #   self.convert_pdf_to_txt(self.path)
      candidates = self.known([word]) or self.known(self.edits1(word)) or self.known_edits2(word) or [word]
      return max(candidates, key=self.NWORDS.get)



