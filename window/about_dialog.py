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
        content = wx.StaticText(panel, wx.ID_NEW, "PepperImageLite")
        content.SetFont(font)
        font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        line1 = wx.StaticText(panel, wx.ID_NEW, "数字图像处理大作业")
        line1.SetFont(font)
        line2 = wx.StaticText(panel, wx.ID_NEW, "71115325")
        line2.SetFont(font)
        line3 = wx.StaticText(panel, wx.ID_NEW, "邹迪凯")
        line3.SetFont(font)
        layout.Add(content, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 10)
        layout.Add(line1, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 5)
        layout.Add(line2, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 5)
        layout.Add(line3, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 5)
        panel.SetSizer(layout)
