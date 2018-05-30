import wx


class AbountDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, "关于", style=wx.CAPTION |
                           wx.STAY_ON_TOP | wx.CLOSE_BOX)
        self.__init_widgets()

    def __init_widgets(self):
        panel = wx.Panel(self)
        layout = wx.BoxSizer(wx.VERTICAL)
        font = wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        content = wx.StaticText(panel, wx.ID_NEW, "Doudou PS Lite")
        content.SetFont(font)
        layout.Add(content, 1,  wx.ALIGN_CENTER_HORIZONTAL|wx.TOP, 10)
        panel.SetSizer(layout)
