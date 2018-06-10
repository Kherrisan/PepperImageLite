import wx
import numpy as np
from function import Function


class MedianFilterDialog(wx.Dialog):
    def __init__(self, parent, function: Function, preview_callback, confirm_callback, cancel_callback):
        wx.Dialog.__init__(self, parent, -1, "中值滤波",
                           style=wx.CAPTION | wx.STAY_ON_TOP | wx.CLOSE_BOX)
        self.function = function
        self.preview_callback = preview_callback
        self.confirm_callback = confirm_callback
        self.cancal_callback = cancel_callback
        self.btn_confirm = None
        self.btn_cancle = None
        self.btn_preview = None
        self.slider_size = None
        self.text_ctrl_size = None
        self.__init_widgets()
        self.__init_events()

    def __init_widgets(self):
        panel = wx.Panel(self)
        layout = wx.BoxSizer(wx.VERTICAL)
        stext_sz = wx.StaticText(panel, -1, "窗口大小")
        sz_layout = wx.BoxSizer(wx.HORIZONTAL)
        self.slider_size = wx.Slider(panel, -1, minValue=0, maxValue=10,)
        self.text_ctrl_size = wx.TextCtrl(
            panel, -1, size=(40, 10), style=wx.TE_PROCESS_ENTER)
        self.text_ctrl_size.SetLabelText(str(0))
        sz_layout.Add(stext_sz, 2, wx.ALL, 5)
        sz_layout.Add(self.slider_size, 7, wx.ALL | wx.EXPAND, 5)
        sz_layout.Add(self.text_ctrl_size, 2, wx.ALL | wx.EXPAND, 5)

        self.btn_preview = wx.Button(panel, -1, "预览")
        self.btn_confirm = wx.Button(panel, -1, "确定")
        self.btn_cancel = wx.Button(panel, -1, "取消")
        btns_layout = wx.BoxSizer(wx.HORIZONTAL)
        btns_layout.Add(self.btn_confirm, 1, wx.ALL, 5)
        btns_layout.Add(self.btn_cancel, 1, wx.ALL, 5)
        btns_layout.Add(self.btn_preview, 1, wx.ALL, 5)
        layout.Add(sz_layout, 0, wx.ALL, 5)
        layout.Add(btns_layout, 0, wx.ALL | wx.EXPAND, 5)
        panel.SetSizer(layout)

    def __init_events(self):
        self.Bind(wx.EVT_BUTTON, self.__on_btn_confirm_click, self.btn_confirm)
        self.Bind(wx.EVT_BUTTON, self.__on_btn_cancel_click, self.btn_cancel)
        self.Bind(wx.EVT_BUTTON, self.__on_btn_preview_click, self.btn_preview)
        self.Bind(wx.EVT_SCROLL, self.__on_slider_sz_changed, self.slider_size)
        self.Bind(wx.EVT_TEXT_ENTER, self.__on_text_ctrl_sz_changed,
                  self.text_ctrl_size)

    def __on_slider_sz_changed(self, evt):
        val = self.slider_size.GetValue()
        self.text_ctrl_size.SetValue(str(val))

    def __on_text_ctrl_sz_changed(self, evt):
        label = self.text_ctrl_size.GetLineText(0)
        self.slider_size.SetValue(int(label))

    def __on_btn_confirm_click(self, evt):
        sz = self.text_ctrl_size.GetLineText(0)
        self.function.median_blur(int(sz))
        self.function.checkpoint()
        self.confirm_callback()
        self.Close()

    def __on_btn_preview_click(self, evt):
        sz = self.text_ctrl_size.GetLineText(0)
        self.function.median_blur(int(sz))
        self.preview_callback()

    def __on_btn_cancel_click(self, evt):
        self.function.rollback()
        self.cancal_callback()
        self.Close()
