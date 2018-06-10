import wx
import numpy as np


class SurfaceBlurDialog(wx.Dialog):
    def __init__(self, parent, function, preview_callback, confirm_callback, cancel_callback):
        wx.Dialog.__init__(self, parent, -1, "导向滤波", style=wx.CAPTION |
                           wx.STAY_ON_TOP | wx.CLOSE_BOX)
        self.function = function
        self.preview_callback = preview_callback
        self.confirm_callback = confirm_callback
        self.cancel_callback = cancel_callback
        self.btn_confirm = None
        self.btn_cancel = None
        self.btn_preview = None
        self.slider_length = None
        self.text_ctrl_length = None
        self.slider_direction = None
        self.text_ctrl_direction = None
        self.__init_widgets()
        self.__init_events()

    def __init_events(self):
        self.Bind(wx.EVT_BUTTON, self.__on_btn_confirm_click, self.btn_confirm)
        self.Bind(wx.EVT_BUTTON, self.__on_btn_cancel_click, self.btn_cancel)
        self.Bind(wx.EVT_SCROLL, self.__on_slider_length_changed,
                  self.slider_length)
        self.Bind(wx.EVT_TEXT_ENTER, self.__on_text_ctrl_length_changed,
                  self.text_ctrl_length)
        self.Bind(wx.EVT_SCROLL, self.__on_slider_direction_changed,
                  self.slider_direction)
        self.Bind(wx.EVT_TEXT_ENTER, self.__on_text_ctrl_direction_changed,
                  self.text_ctrl_direction)
        self.Bind(wx.EVT_BUTTON, self.__on_btn_preview_click, self.btn_preview)

    def __on_text_ctrl_length_changed(self, event):
        label = self.text_ctrl_length.GetLineText(0)
        self.slider_length.SetValue(int(label))

    def __on_slider_length_changed(self, event):
        val = self.slider_length.GetValue()
        self.text_ctrl_length.SetLabelText(str(val))

    def __on_slider_direction_changed(self, event):
        val = self.slider_direction.GetValue()
        self.text_ctrl_direction.SetLabelText(str(val))

    def __on_text_ctrl_direction_changed(self, event):
        label = self.text_ctrl_direction.GetLineText(0)
        self.slider_direction.SetValue(float(label))

    def __on_btn_preview_click(self, event):
        length = self.text_ctrl_length.GetLineText(0)
        theta = self.text_ctrl_direction.GetLineText(0)
        self.function.guided_filter(int(length), float(theta))
        self.preview_callback()

    def __on_btn_confirm_click(self, event):
        length = self.text_ctrl_length.GetLineText(0)
        theta = self.text_ctrl_direction.GetLineText(0)
        self.function.guided_filter(int(length), float(theta))
        self.function.checkpoint()
        self.confirm_callback()
        self.Close()

    def __on_btn_cancel_click(self, event):
        self.function.rollback()
        self.cancel_callback()
        self.Close()

    def __init_widgets(self):
        panel = wx.Panel(self)
        layout = wx.BoxSizer(wx.VERTICAL)
        stext_length = wx.StaticText(panel, -1, "半径")
        stext_direction = wx.StaticText(panel, -1, "正则项")
        length_layout = wx.BoxSizer(wx.HORIZONTAL)
        self.slider_length = wx.Slider(
            panel, -1, minValue=0, maxValue=100)
        self.text_ctrl_length = wx.TextCtrl(
            panel, -1, size=(40, 10), style=wx.TE_PROCESS_ENTER)
        self.text_ctrl_length.SetLabelText(str(0))
        length_layout.Add(stext_length, 1, wx.ALL, 5)
        length_layout.Add(self.slider_length, 9, wx.ALL | wx.EXPAND, 5)
        length_layout.Add(self.text_ctrl_length, 1, wx.ALL | wx.EXPAND, 5)

        direction_layout = wx.BoxSizer(wx.HORIZONTAL)
        self.slider_direction = wx.Slider(
            panel, -1, minValue=0, maxValue=300)
        self.text_ctrl_direction = wx.TextCtrl(
            panel, -1, size=(40, 10), style=wx.TE_PROCESS_ENTER)
        self.text_ctrl_direction.SetLabelText(str(0))
        direction_layout.Add(stext_direction, 1, wx.ALL, 5)
        direction_layout.Add(self.slider_direction, 9, wx.ALL | wx.EXPAND, 5)
        direction_layout.Add(self.text_ctrl_direction,
                             1, wx.ALL | wx.EXPAND, 5)

        self.btn_preview = wx.Button(panel, -1, "预览")
        self.btn_confirm = wx.Button(panel, -1, "确定")
        self.btn_cancel = wx.Button(panel, -1, "取消")
        btns_layout = wx.BoxSizer(wx.HORIZONTAL)
        btns_layout.Add(self.btn_confirm, 1, wx.ALL, 5)
        btns_layout.Add(self.btn_cancel, 1, wx.ALL, 5)
        btns_layout.Add(self.btn_preview, 1, wx.ALL, 5)
        layout.Add(length_layout, 0, wx.ALL, 5)
        layout.Add(direction_layout, 0, wx.ALL, 5)
        layout.Add(btns_layout, 0, wx.ALL | wx.EXPAND, 5)
        panel.SetSizer(layout)
