import wx
import os
from top import top
#import wx.Image
import wx.lib.wxcairo as wxcairo
import sys
# import poppler
# import matplotlib.pyplot as plt
picturewidth=600
pictureheight=600
class PDFWindow(wx.ScrolledWindow):
    """ This example class implements a PDF Viewer Window, handling Zoom and Scrolling """

    MAX_SCALE = 2
    MIN_SCALE = 1
    SCROLLBAR_UNITS = 20  # pixels per scrollbar unit

    def __init__(self, parent):
        wx.ScrolledWindow.__init__(self, parent, wx.ID_ANY,size=(600,600))
        # Wrap a panel inside
        self.panel = wx.Panel(self)
        # Initialize variables
        self.n_page = 0
        self.scale = 1
        self.document = None
        self.n_pages = None
        self.current_page = None
        self.width = None
        self.height = None
        # Connect panel events
        self.pdfwindow = None
        self.panel.Bind(wx.EVT_PAINT, self.OnPaint)
        self.panel.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.panel.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.panel.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)

    def LoadDocument(self, file):
        self.document = poppler.document_new_from_file("file://" + file, None)
        self.n_pages = self.document.get_n_pages()
        self.current_page = self.document.get_page(self.n_page)
        self.width, self.height = self.current_page.get_size() 
        self._UpdateSize()

    def OnPaint(self, event):
        dc = wx.PaintDC(self.panel)
        cr = wxcairo.ContextFromDC(dc)
        cr.set_source_rgb(1, 1, 1)  # White background
        if self.scale != 1:
            cr.scale(self.scale, self.scale)
        cr.rectangle(0.0, 0.0, self.width, self.height)
        cr.fill()
        self.current_page.render(cr)

    def OnLeftDown(self, event):
        self._UpdateScale(self.scale + 0.2)

    def OnRightDown(self, event):
        self._UpdateScale(self.scale - 0.2)

    def _UpdateScale(self, new_scale):
        if new_scale >= PDFWindow.MIN_SCALE and new_scale <= PDFWindow.MAX_SCALE:
            self.scale = new_scale
            # Obtain the current scroll position
            prev_position = self.GetViewStart() 
            # Scroll to the beginning because I'm going to redraw all the panel
            self.Scroll(0, 0) 
            # Redraw (calls OnPaint and such)
            self.Refresh() 
            # Update panel Size and scrollbar config
            self._UpdateSize()
            # Get to the previous scroll position
            self.Scroll(prev_position[0], prev_position[1]) 

    def _UpdateSize(self):
        u = PDFWindow.SCROLLBAR_UNITS
        self.panel.SetSize((self.width*self.scale, self.height*self.scale))
        self.SetScrollbars(u, u, (self.width*self.scale)/u, (self.height*self.scale)/u)

    def OnKeyDown(self, event):
        update = True
        # More keycodes in http://docs.wxwidgets.org/stable/wx_keycodes.html#keycodes
        keycode = event.GetKeyCode() 
        if keycode in (wx.WXK_PAGEDOWN, wx.WXK_SPACE):
            next_page = self.n_page + 1
        elif keycode == wx.WXK_PAGEUP:
            next_page = self.n_page - 1
        else:
            update = False
        if update and (next_page >= 0) and (next_page < self.n_pages):
                self.n_page = next_page
                self.current_page = self.document.get_page(next_page)
                self.Refresh()


# class MyFrame(wx.Frame):
 
#     def __init__(self):
#         wx.Frame.__init__(self, None, -1, "wxPdf Viewer", size=(800,600))
#         self.pdfwindow = PDFWindow(self)
#         self.pdfwindow.LoadDocument(sys.argv[1])
#         self.pdfwindow.SetFocus() # To capture keyboard events

 
# if __name__=="__main__":
#     app = wx.App()
#     f = MyFrame()
#     f.Show()
#     app.MainLoop()
class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, None, -1, "Opensoft16",size=(1000,600))
        self.dirname=''
        self.current_files=[]
        self.processed_files=[]
        self.processor=top()
        self.currentdoc=None
        #self.pdfwindow = PDFWindow(self)
        img = wx.EmptyImage(pictureheight,picturewidth)
        self.rightpanel = wx.Panel(self)
        self.leftpanel = wx.Panel(self)
        self.imageCtrl = wx.StaticBitmap(self.rightpanel, wx.ID_ANY, 
                                         wx.BitmapFromImage(img))
        #self.treemap={}
        # A "-1" in the size parameter instructs wxWidgets to use the default size.
        # In this case, we select 200px width and the default height.
        #wx.Frame.__init__(self, parent, title=title, size=(200,-1))
        #self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.CreateStatusBar() # A Statusbar in the bottom of the window
        #tree
        self.tree_ctrl = wx.TreeCtrl(self, -1, style=wx.TR_DEFAULT_STYLE | \
                                                wx.TR_FULL_ROW_HIGHLIGHT )
        self.root = self.tree_ctrl.AddRoot('Files')
        #self.tree_ctrl.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, id=1)
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

        # Events.
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)

        self.sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer3.Add(self.rightpanel,1,wx.EXPAND)
        #self.buttons = []
        #for i in range(0, 6):
        #    self.buttons.append(wx.Button(self, -1, "Button &"+str(i)))
        #    self.sizer2.Add(self.buttons[i], 1, wx.EXPAND)

        # Use some sizers to see layout options
        self.sizer2=wx.BoxSizer(wx.VERTICAL)
        #self.sizer2.Add(self.pdfwindow, 1, wx.EXPAND)
        self.sizer2.Add(self.sizer3, 1, wx.EXPAND)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.tree_ctrl, 1, wx.EXPAND)
        self.sizer.Add(self.sizer2,1,wx.EXPAND)
        #self.sizer.Add(self.sizer2, 0, wx.EXPAND)

        #Layout sizers
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)
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
            self.current_files=dlg.GetPaths()
            self.processed_files=self.processor.do(self.current_files)
            #self.tree_ctrl = wx.TreeCtrl(self, -1, style=wx.TR_DEFAULT_STYLE | \
            #                                    wx.TR_FULL_ROW_HIGHLIGHT )
            #self.root = self.tree_ctrl.AddRoot('Files')
            self.reinit()
            self.leftpanel.Refresh()
            self.tree_ctrl.ExpandAll()
            self.sizer.Fit(self)
        dlg.Destroy()
    def reinit(self):
        cntdoc=1
        for doc in self.processed_files:
            currentdoc=self.tree_ctrl.AppendItem(self.root,"doc_"+str(cntdoc))
           #print currentdoc.GetID()
            #self.treemap[currentdoc]=doc
            self.tree_ctrl.SetItemPyData(currentdoc, doc)
            print currentdoc.__class__.__name__
            cntdoc=cntdoc+1
            cntpage=1
            for page in doc.pageList:
                currentpage= self.tree_ctrl.AppendItem(currentdoc,"Page_"+str(cntpage))
                cntpage=cntpage+1
                #self.treemap[currentpage]=page
                self.tree_ctrl.SetItemPyData(currentpage, page)
                cntgraph=1
                for gr in page.graphList:
                    currentgraph=self.tree_ctrl.AppendItem(currentpage,"Graph_"+str(cntgraph))
                    self.tree_ctrl.SetItemPyData(currentgraph, gr)
                    cntgraph=cntgraph+1
                    #tempimage=Image(gr.image.toString())
                    #self.sizer2.Add(tempimage,1,wx.EXPAND)
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
            pass
        if obj.__class__.__name__=='page':
            print 'page'
            image=obj.pdfImage
            h, w = image.shape[:2]
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
            wxImage = wx.ImageFromBuffer( w,h, image)
            wxImage=wxImage.Scale(W,H)
            print W
            print H
            bitmap = wx.BitmapFromImage(wxImage)
            self.imageCtrl = wx.StaticBitmap(self.rightpanel, wx.ID_ANY,bitmap)
            self.rightpanel.Refresh()
        if obj.__class__.__name__=='graph':
            print 'graph'
            image=obj.image
            plt.subplot(1,1,1),plt.imshow(image)
            plt.show()
            h, w = image.shape[:2]
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
            wxImage = wx.ImageFromBuffer( w,h, image)
            wxImage=wxImage.Scale(W,H)
            print W
            print H
            bitmap = wx.BitmapFromImage(wxImage)
            self.imageCtrl = wx.StaticBitmap(self.rightpanel, wx.ID_ANY,bitmap)
            self.rightpanel.Refresh()


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
        app = wx.App(False)
        frame = MainWindow(None, "Sample editor")
        app.MainLoop()