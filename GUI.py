import wx
import os
from top import top
#import wx.Image
class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        self.dirname=''
        self.current_files=[]
        self.processed_files=[]
        self.processor=top()
        # A "-1" in the size parameter instructs wxWidgets to use the default size.
        # In this case, we select 200px width and the default height.
        wx.Frame.__init__(self, parent, title=title, size=(200,-1))
        #self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.CreateStatusBar() # A Statusbar in the bottom of the window
        #tree
        self.tree_ctrl = wx.TreeCtrl(self, -1, style=wx.TR_DEFAULT_STYLE | \
                                                wx.TR_FULL_ROW_HIGHLIGHT | \
                                                wx.TR_EDIT_LABELS)
        self.root = self.tree_ctrl.AddRoot('Files')
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

        #self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        #self.buttons = []
        #for i in range(0, 6):
        #    self.buttons.append(wx.Button(self, -1, "Button &"+str(i)))
        #    self.sizer2.Add(self.buttons[i], 1, wx.EXPAND)

        # Use some sizers to see layout options
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.tree_ctrl, 1, wx.EXPAND)

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
        dlg = wx.FileDialog(self, "Choose files", self.dirname, ".", "*.*", wx.FD_MULTIPLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.current_files=dlg.GetPaths()
            self.processed_files=self.processor.do(self.current_files)
            self.reinit()
            self.tree_ctrl.ExpandAll()
            self.sizer.Fit(self)
        dlg.Destroy()
    def reinit(self):
        cntdoc=1
        for doc in self.processed_files:
            currentdoc=self.tree_ctrl.AppendItem(self.root,"doc_"+str(cntdoc))
            cntdoc=cntdoc+1
            cntpage=1
            for page in doc.pageList:
                currentpage= self.tree_ctrl.AppendItem(currentdoc,"Page_"+str(cntpage))
                cntpage=cntpage+1
                cntgraph=1
                for gr in page.graphList:
                    self.tree_ctrl.AppendItem(currentpage,"Graph_"+str(cntgraph))
                    cntgraph=cntgraph+1
                    #tempimage=Image(gr.image.toString())
                    #self.sizer2.Add(tempimage,1,wx.EXPAND)


app = wx.App(False)
frame = MainWindow(None, "Sample editor")
app.MainLoop()