import wx
import os
from top import top
#import wx.Image
import wx.lib.wxcairo as wxcairo
import sys
import cv2
import poppler
from graph import graph
from curve import curve
from document import document
from page import page
picturewidth=300
pictureheight=300
pagewidth=600
pageheight=600
class curvepanel(wx.Panel):
	def __init__(self,parent,curveobj):
		wx.Panel.__init__(self,parent)
		self.fulsizer=wx.BoxSizer(wx.VERTICAL)
		self.curve=curveobj
		self.titlesizer=wx.BoxSizer(wx.HORIZONTAL)
		self.titlabel=wx.StaticText(self,-1,"Title:")
		self.inputtitle=wx.TextCtrl(self)
		self.inputtitle.AppendText(self.curve.name)
		self.titlesizer.Add(self.titlabel,1,wx.EXPAND)
		self.titlesizer.Add(self.inputtitle,1,wx.EXPAND)

		self.tabletext=wx.TextCtrl(self,style=wx.TE_MULTILINE)
		for i in range(0,len(self.curve.x)):
			self.tabletext.append(str(self.curve.x[i]+" : "+str(self.curve.y[i])))
		self.fulsizer.Add(self.titlesizer)
		self.fulsizer.Add(self.tabletext)
		self.SetSizer(self.fulsizer)

class CurveNoteBook(wx.Notebook):
    """
    Notebook class
    """
 
    #----------------------------------------------------------------------
    def __init__(self, parent,curvelist):
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=
                             wx.BK_DEFAULT
                             #wx.BK_TOP 
                             #wx.BK_BOTTOM
                             #wx.BK_LEFT
                             #wx.BK_RIGHT
                             )
 
        # Create the first tab and add it to the notebook
        for curve in curvelist:
        	curvetab=curvepanel(self,curve)
        	#curvetab.SetBackgroundColour("Gray")
        	self.AddPage(curvetab, curve.name)

class GraphNoteBook(wx.Notebook):
    """
    Notebook class
    """
 
    #----------------------------------------------------------------------
    def __init__(self, parent,graphlist):
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=
                             wx.BK_DEFAULT
                             #wx.BK_TOP 
                             #wx.BK_BOTTOM
                             #wx.BK_LEFT
                             #wx.BK_RIGHT
                             )
        for graph in graphlist:
        	graphtab=grPanel(self,graph)
        	#curvetab.SetBackgroundColour("Gray")
        	self.AddPage(graphtab, "Graph")
 
        # Create the first tab and add it to the notebook
    	


class grPanel(wx.Panel):
	def __init__(self,parent,graphobj):
		wx.Panel.__init__(self,parent)
		self.sizer=wx.BoxSizer(wx.VERTICAL)
		#self.sizer2=wx.BoxSizer(wx.HORIZONTAL)
		#self.curvepanels=[]
		self.xlabelsizer=wx.BoxSizer(wx.HORIZONTAL)
		self.xlabellabel=wx.StaticText(self,-1,"Xlabel:")
		self.inputxlabel=wx.TextCtrl(self)
		self.inputxlabel.AppendText(str(graphobj.xlabel))
		self.xlabelsizer.Add(self.xlabellabel,1,wx.EXPAND)
		self.xlabelsizer.Add(self.inputxlabel,1,wx.EXPAND)
		
		self.ylabelsizer=wx.BoxSizer(wx.HORIZONTAL)
		self.ylabellabel=wx.StaticText(self,-1,"Ylabel:")
		self.inputylabel=wx.TextCtrl(self)
		self.inputylabel.AppendText(str(graphobj.ylabel))
		self.ylabelsizer.Add(self.ylabellabel,1,wx.EXPAND)
		self.ylabelsizer.Add(self.inputylabel,1,wx.EXPAND)
		
		self.minxsizer=wx.BoxSizer(wx.HORIZONTAL)
		self.minxlabel=wx.StaticText(self,-1,"Minx:")
		self.inputminx=wx.TextCtrl(self)
		self.inputminx.AppendText(str(graphobj.minx))
		self.minxsizer.Add(self.minxlabel,1,wx.EXPAND)
		self.minxsizer.Add(self.inputminx,1,wx.EXPAND)
		
		self.minysizer=wx.BoxSizer(wx.HORIZONTAL)
		self.minylabel=wx.StaticText(self,-1,"miny:")
		self.inputminy=wx.TextCtrl(self)
		self.inputminy.AppendText(str(graphobj.miny))
		self.minysizer.Add(self.minylabel,1,wx.EXPAND)
		self.minysizer.Add(self.inputminy,1,wx.EXPAND)
		
		self.maxxsizer=wx.BoxSizer(wx.HORIZONTAL)
		self.maxxlabel=wx.StaticText(self,-1,"maxx:")
		self.inputmaxx=wx.TextCtrl(self)
		self.inputmaxx.AppendText(str(graphobj.maxx))
		self.maxxsizer.Add(self.maxxlabel,1,wx.EXPAND)
		self.maxxsizer.Add(self.inputmaxx,1,wx.EXPAND)
		
		self.maxysizer=wx.BoxSizer(wx.HORIZONTAL)
		self.maxylabel=wx.StaticText(self,-1,"maxy:")
		self.inputmaxy=wx.TextCtrl(self)
		self.inputmaxy.AppendText(str(graphobj.maxy))
		self.maxysizer.Add(self.maxylabel,1,wx.EXPAND)
		self.maxysizer.Add(self.inputmaxy,1,wx.EXPAND)
		
		image=graphobj.rectangle
		cv2.imwrite('temp.jpg',image)
		image=wx.Image('temp.jpg')
            	h= image.Height
            	w=image.Width
            #wxImage = wx.ImageFromBuffer(w, h, image)
            	H=h
            	W=w
            	if(h>pictureheight):
             	   	H=pictureheight
              	  	W=(pictureheight*w)/h
            	if(W>picturewidth):
              	  H=(picturewidth*H)/W
              	  W=picturewidth
            #newimage=np.zeros((H,W,3), np.uint8)
            #newimage=cv2.resize(image,(H,W))
            #image=newimage
            	#wxImage = wx.BitmapFromBuffer( w,h, image)
            	wxImage=image.Scale(W,H)
            	print W
            	print H
            	bitmap = wx.BitmapFromImage(wxImage)
            	self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY,bitmap)
    		self.sizer.Add(self.xlabelsizer)
    		self.sizer.Add(self.ylabelsizer)
    		self.sizer.Add(self.minxsizer)
    		self.sizer.Add(self.maxxsizer)
    		self.sizer.Add(self.minysizer)
    		self.sizer.Add(self.maxysizer)
    		self.sizer.Add(self.imageCtrl)
		#self.titlabel=wx.StaticText(self,-1,"Title:")
		self.graph=graphobj
		self.curvenote=CurveNoteBook(self,graphobj.curveList)
		# h, w = graphobj.image.shape[:2]
  #       #wxImage = wx.ImageFromBuffer(w, h, image)
  #       H=h
  #       W=w
  #       if(h>pictureheight):
  #           H=pictureheight
  #           W=(pictureheight*w)/h
  #       if(W>picturewidth):
  #           H=(picturewidth*H)/W
  #           W=picturewidth
  #       #newimage=np.zeros((H,W,3), np.uint8)
  #       #newimage=cv2.resize(image,(H,W))
  #       #image=newimage
  #       wxImage = wx.ImageFromBuffer( w,h, graphobj.image)
  #       wxImage=wxImage.Scale(W,H)
  #       print W
  #       print H
  #       bitmap = wx.BitmapFromImage(wxImage)
  #       self.imageCtrl = wx.StaticBitmap(self.rightpanel, wx.ID_ANY,bitmap)
  #       self.sizer.Add(self.imageCtrl,1,wx.EXPAND)
        #self.Refresh()
		#self.sizer.Add(self.sizer2,1,wx.EXPAND)
		#self.sizer.Add(self.titlabel,1,wx.EXPAND)
		self.sizer.Add(self.curvenote,1,wx.EXPAND)
    		self.SetSizer(self.sizer)
    		print 'yo'
		# ht, wt = graphobj.image.shape[:2]
  #       #wxImage = wx.ImageFromBuffer(w, h, image)
  #       H=ht
  #       W=wt
  #       if(ht>pictureheight):
  #           H=pictureheight
  #           W=(pictureheight*wt)/ht
  #       if(W>picturewidth):
  #           H=(picturewidth*H)/W
  #           W=picturewidth
  #       #newimage=np.zeros((H,W,3), np.uint8)
  #       #newimage=cv2.resize(image,(H,W))
  #       #image=newimage
  #       wxImage = wx.ImageFromBuffer( w,h, graphobj.image)
  #       wxImage=wxImage.Scale(W,H)
  #       print W
  #       print H
  #       bitmap = wx.BitmapFromImage(wxImage)
  #       self.imageCtrl = wx.StaticBitmap(self.rightpanel, wx.ID_ANY,bitmap)
  #       self.sizer.Add(self.imageCtrl,1,wx.EXPAND)
        #self.Refresh()
class pagePanel(wx.Panel):
	def __init__(self,parent,page):
		print '3'
		wx.Panel.__init__(self,parent)
		self.page=page
		#self.pageviewnote=wx.Notebook(self)
		self.graphnote=GraphNoteBook(self,page.graphList)
		self.panel1=wx.Panel(self.graphnote)
		image=page.pdfImage
		cv2.imwrite('temp.jpg',image)
		image=wx.Image('temp.jpg')
            	h= image.Height
            	w=image.Width
            #wxImage = wx.ImageFromBuffer(w, h, image)
            	H=h
            	W=w
            	if(h>pageheight):
             	   	H=pageheight
              	  	W=(pageheight*w)/h
            	if(W>pagewidth):
              	  H=(pagewidth*H)/W
              	  W=pagewidth
            #newimage=np.zeros((H,W,3), np.uint8)
            #newimage=cv2.resize(image,(H,W))
            #image=newimage
            	#wxImage = wx.BitmapFromBuffer( w,h, image)
            	wxImage=image.Scale(W,H)
            	print W
            	print H
            	bitmap = wx.BitmapFromImage(wxImage)
            	self.imageCtrl = wx.StaticBitmap(self.panel1, wx.ID_ANY,bitmap)
		self.graphnote.AddPage(self.panel1,"PageView")
		self.sizer=wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add(self.graphnote,1,wx.EXPAND)
    		self.SetSizer(self.sizer)

class PageNoteBook(wx.Notebook):
    """
    Notebook class
    """
 
    #----------------------------------------------------------------------
    def __init__(self, parent,pagelist):
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=
                             wx.BK_DEFAULT
                             #wx.BK_TOP 
                             #wx.BK_BOTTOM
                             #wx.BK_LEFT
                             #wx.BK_RIGHT
                             )
        print '2'
        for page in pagelist:
        	pagetab=pagePanel(self,page)
        	#curvetab.SetBackgroundColour("Gray")
        	self.AddPage(pagetab, "Page")
 
        # Create the first tab and add it to the notebook
class docPanel(wx.Panel):
	def __init__(self,parent,docu):
		
		wx.Panel.__init__(self,parent)
		self.doc=docu
		self.pagenote=PageNoteBook(self,docu.pageList)
		self.sizer=wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add(self.pagenote,1,wx.EXPAND)
    		self.SetSizer(self.sizer)


class DocNoteBook(wx.Notebook):
    """
    Notebook class
    """
    print 'here'
    #----------------------------------------------------------------------
    def __init__(self, parent,doclist):
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=
                             wx.BK_DEFAULT
                             #wx.BK_TOP 
                             #wx.BK_BOTTOM
                             #wx.BK_LEFT
                             #wx.BK_RIGHT
                             )
        self.initdocs(doclist)
    def initdocs(self,doclist):
        for doc in doclist:
        	print '1'
        	doctab=docPanel(self,doc)
        	#curvetab.SetBackgroundColour("Gray")
        	self.AddPage(doctab, "Document")
        # Create the first tab and add it to the notebook
class DemoFrame(wx.Frame):
    """
    Frame that holds all other widgets
    """
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "Notebook Tutorial",
                          size=(600,400)
                          )
        panel = wx.Panel(self)
        self.obj=document()
        self.obj.pageList=[page(1,1)]
        lis=[self.obj, self.obj, self.obj]
        notebook = DocNoteBook(panel,lis)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.ALL|wx.EXPAND, 5)
        panel.SetSizer(sizer)
        self.Layout()
 
        self.Show()
 
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = DemoFrame()
    app.MainLoop()
