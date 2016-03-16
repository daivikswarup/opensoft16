import wx
import os
from top import top
#import wx.Image
import wx.lib.wxcairo as wxcairo
import sys
from grPanel import *
import threading
from document import document
from Utils import ResultEvent,EVT_RESULT_ID
# import poppler
# import matplotlib.pyplot as plt
picturewidth=600
pictureheight=600


def EVT_RESULT(win, func):
   """Define Result Event."""
   win.Connect(-1, -1, EVT_RESULT_ID, func)

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, None, -1, "Opensoft16",size=(1000,600))
        self.dirname=''
        self.docList=[]
        self.currentdoc=None

        # refresh UI
        EVT_RESULT(self,self.OnResult)

        self.initUI()

    def initUI(self):
        self.CreateStatusBar()
        
        #Notebook
        self.docnote=DocNoteBook(self,self.docList)

        #tree
        self.tree_ctrl = wx.TreeCtrl(self, -1, style=wx.TR_DEFAULT_STYLE | \
                                                wx.TR_FULL_ROW_HIGHLIGHT )
        self.root = self.tree_ctrl.AddRoot('Files')
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivated, self.tree_ctrl)

        # Setting up the menu.
        filemenu= wx.Menu()
        menuOpen = filemenu.Append(wx.ID_OPEN, "&Open"," Open a file to edit")
        menuAbout= filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        # Events for menu
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        
        #Sizer
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.tree_ctrl, 1, wx.EXPAND)
        self.sizer.Add(self.docnote, 1, wx.EXPAND)

        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.Show()

    def OnAbout(self,e):
        # Create a message dialog box
        dlg = wx.MessageDialog(self, " To extract tables from graphs", wx.OK)
        dlg.ShowModal() # Shows it
        dlg.Destroy() # finally destroy it when finished.

    def OnExit(self,e):
        self.Close(True)  # Close the frame.

    def OnOpen(self,e):
        """ Open a file"""
        dlg = wx.FileDialog(self, "Choose files", self.dirname, ".", "*.pdf", wx.FD_MULTIPLE)
        if dlg.ShowModal() == wx.ID_OK:
        #ProgressBar

            self.totalpages=0
            self.pagesdone=0
            self.progress=wx.ProgressDialog('Progress','Starting...')
            for address in dlg.GetPaths():
                d = document(self,address,len(self.docList))
                d.start()
                self.docList.append(d)
            self.RefreshTree()
            # for d in self.docList:
            #     d.join()
            #self.tree_ctrl = wx.TreeCtrl(self, -1, style=wx.TR_DEFAULT_STYLE | \
            #                                    wx.TR_FULL_ROW_HIGHLIGHT )
            #self.root = self.tree_ctrl.AddRoot('Files')
            
            #self.tree_ctrl.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, id=1)

        dlg.Destroy()

    def OnResult(self,event):
        if event.data is 10:
            self.RefreshTree()
        if event.data is 5:
            self.pagesdone=self.pagesdone+1
            self.progress.Update((self.pagesdone*100)/self.totalpages,str(self.pagesdone)+'/'+str(self.totalpages)+' pages done')
            if self.pagesdone==self.totalpages:
                self.progress.Destroy()
        if event.data is 15:
            self.totalpages=self.totalpages+1
            self.progress.Update((self.pagesdone*100)/self.totalpages,str(self.pagesdone)+'/'+str(self.totalpages)+' pages done')

    def RefreshTree(self):
        print"Refreshing Tree"
        self.tree_ctrl.DeleteAllItems()
        self.root = self.tree_ctrl.AddRoot('Files')
        cntdoc=0
        #self.sizer.Remove(self.docnote)
        self.docnote.initdocs(self.docList)        #self.rightpanel.Refresh()
        #self.sizer.Add(self.docnote,1,wx.EXPAND)
        #self.rightsizer.Add(self.docnote,wx.ALL|wx.EXPAND, 5)
        print 'here'
        for doc in self.docList:
            currentdoc=self.tree_ctrl.AppendItem(self.root,"doc_"+str(cntdoc))
           #print currentdoc.GetID()
            #self.treemap[currentdoc]=doc
            doc.docid=cntdoc
            self.tree_ctrl.SetItemPyData(currentdoc, doc)
            #print currentdoc.__class__.__name__
            cntdoc=cntdoc+1
            cntpage=1
            print 'x'
            for page in doc.pageList:
                currentpage= self.tree_ctrl.AppendItem(currentdoc,"Page_"+str(cntpage))
                cntpage=cntpage+1
                #self.treemap[currentpage]=page
                self.tree_ctrl.SetItemPyData(currentpage, page)
                cntgraph=1
                print 'yo'
                for gr in page.graphList:
                    currentgraph=self.tree_ctrl.AppendItem(currentpage,"Graph_"+str(cntgraph))
                    self.tree_ctrl.SetItemPyData(currentgraph, gr)
                    cntgraph=cntgraph+1
                    #tempimage=Image(gr.image.toString())
                    #self.sizer2.Add(tempimage,1,wx.EXPAND)
        #self.leftpanel.Refresh()
        self.tree_ctrl.ExpandAll()
        self.sizer.Fit(self)
        
    def OnSelChanged(self, event):
        '''Method called when selected item is changed
        '''
        # Get the selected item object
        print 'here'
        item =  event.GetItem()
        print item
    def OnActivated(self, evt):
        print "OnActivated:    "
        obj=self.tree_ctrl.GetItemData(evt.GetItem()).GetData()
        if obj.__class__.__name__=='document':
            self.docnote.SetSelection(obj.docid)
        if obj.__class__.__name__=='page':
            self.docnote.SetSelection(obj.document.docid)
            self.docnote.pages[obj.document.docid].pagenote.SetSelection(obj.pageno)
            # print 'page'
            # image=obj.pdfImage
            # h, w = image.shape[:2]
            # #wxImage = wx.ImageFromBuffer(w, h, image)
            # H=h
            # W=w
            # if(h>pictureheight):
            #     H=pictureheight
            #     W=(pictureheight*w)/h
            # if(W>picturewidth):
            #     H=(picturewidth*H)/W
            #     W=picturewidth
            # #newimage=np.zeros((H,W,3), np.uint8)
            # #newimage=cv2.resize(image,(H,W))
            # #image=newimage
            # wxImage = wx.ImageFromBuffer( w,h, image)
            # wxImage=wxImage.Scale(W,H)
            # print W
            # print H
            # bitmap = wx.BitmapFromImage(wxImage)
            # self.imageCtrl = wx.StaticBitmap(self.rightpanel, wx.ID_ANY,bitmap)
            # self.rightpanel.Refresh()
        if obj.__class__.__name__=='graph':
            self.docnote.SetSelection(obj.document.docid)
            self.docnote.pages[obj.document.docid].pagenote.SetSelection(obj.pageno)
            self.docnote.pages[obj.document.docid].pagenote.pages[obj.pageno].graphnote.SetSelection(obj.graphID)
            #self.docnote.pages[obj.document.docid].paged[obj.pageno.SetSelection()
            # print 'graph'
            # image=obj.image
            # plt.subplot(1,1,1),plt.imshow(image)
            # plt.show()
            # h, w = image.shape[:2]
            # #wxImage = wx.ImageFromBuffer(w, h, image)
            # H=h
            # W=w
            # if(h>pictureheight):
            #     H=pictureheight
            #     W=(pictureheight*w)/h
            # if(W>picturewidth):
            #     H=(picturewidth*H)/W
            #     W=picturewidth
            # #newimage=np.zeros((H,W,3), np.uint8)
            # #newimage=cv2.resize(image,(H,W))
            # #image=newimage
            # wxImage = wx.ImageFromBuffer( w,h, image)
            # wxImage=wxImage.Scale(W,H)
            # print W
            # print H
            # bitmap = wx.BitmapFromImage(wxImage)
            # self.imageCtrl = wx.StaticBitmap(self.rightpanel, wx.ID_ANY,bitmap)
            # self.rightpanel.Refresh()


#     def OnBeginDrag(self, event):
#       """ Left Mouse Button initiates "Drag" for Tree Nodes """
#       print 'here'
#       # Items in the tree are not automatically selected with a left click.
#       # We must select the item that is initially clicked manually!!
#       # We do this by looking at the screen point clicked and applying the tree's
#       # HitTest method to determine the current item, then actually selecting the item
#       sel_item, flags = self.tree_ctrl.HitTest(event.GetPoint())
#       self.tree_ctrl.SelectItem(sel_item)
#       print sel_item
#       # Determine what Item is being "dragged", and grab it's data
# #       tempStr = "%s" % (self.tree.GetItemText(sel_item))
# #       print "A node called %s is being dragged" % (tempStr)

# #       # Create a custom Data Object for Drag and Drop
# #       ddd = TestDragDropData()
# #       # In this case, the data is trivial, but this could easily be a more complex object.
# #       ddd.SetSource(tempStr)

# #       # Use cPickle to convert the data object into a string representation
# #       pddd = cPickle.dumps(ddd, 1)

# #       # Now create a wxCustomDataObject for dragging and dropping and
# #       # assign it a custom Data Format
# #       cdo = wx.wxCustomDataObject(wx.wxCustomDataFormat('TransanaData'))
# #       # Put the pickled data object in the wxCustomDataObject
# #       cdo.SetData(pddd)

# #       # Sorry, I am not able to figure out how to extract data from a wxDataObjectComposite until after
# #       # it's been dropped, so I'm ignoring that aspect of things for now.  I've left the code commented
# #       # out for others who wish to pursue it.

# #       # Now put the CustomDataObject into a DataObjectComposite
# # #      tdo = wx.wxDataObjectComposite()
# # #      tdo.Add(cdo)

# #       # Create a Custom DropSource Object.  The custom drop source object
# #       # accepts the tree as a parameter so it can query it about where the
# #       # drop is supposed to be occurring to see if it will allow the drop.
# #       tds = TestDropSource(self.tree)
# #       # Associate the Data with the Drop Source Object
# #       # I've associated both the pickled CustomDataObject and the raw data object here
# #       # so that I can easily work with the data being dragged.  I'm sure this is poor
# #       # form and unnecessary, but there it is.  You don't like it, you are welcome to fix it!
# #       tds.SetData(cdo, ddd)    # (tdo) would be used in place of (cdo) if I were using the DataObjectComposite object

# #       # Initiate the Drag Operation
# #       dragResult = tds.DoDragDrop(wx.true)

# #       # Report the result of the final drop when everything else is completed by the other objects
# #       if dragResult == wx.wxDragCopy:
# #           print "Result indicated successful copy"
# #       elif dragResult == wx.wxDragMove:
# #           print "Result indicated successful move"
# #       else:
# #           print "Result indicated failed drop"
# #       print

class Grapher:

    def run(self):
        print 'here'
        app = wx.App(False)
        frame = MainWindow(None, "Sample editor")
        app.MainLoop()