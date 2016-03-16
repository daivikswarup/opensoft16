import wx

EVT_RESULT_ID = wx.NewId()
class ResultEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""
    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data
DELETE_ID = wx.NewId()
class DeleteEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""
    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(DELETE_ID)
        self.data = data
CROP_ID = wx.NewId()
class CropEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""
    def __init__(self, graph, new_image):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(DELETE_ID)
        self.graph=graph
        self.new_image=new_image