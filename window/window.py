#!/usr/bin/env python
# coding=utf-8
import wx
from window.about_dialog import AbountDialog
from window.motion_blur_dialog import MotionBlurDialog
from function import Function
import os


class MainWindow(wx.Frame):
    def __init__(self, function: Function):
        wx.Frame.__init__(self, None, title="Doudou PS Lite", pos=wx.DefaultPosition, size=wx.Size(
            600, 600), style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        self.IMAGE_WIDTH = 560
        self.IMAGE_HEIGHT = 560
        self.btn_open = None
        self.btn_save = None
        self.btn_save_as = None
        self.btn_undo = None
        self.btn_redo = None
        self.btn_quit = None
        self.btn_about = None
        self.main_layout = None
        self.static_bmp = None
        self.function = function
        self.__init_widgets()
        self.__init_events()
        self.SetSize((600, 601))

    def __init_events(self):
        self.Bind(wx.EVT_MENU, self.__on_btn_about_click, self.btn_about)
        self.Bind(wx.EVT_MENU, self.__on_btn_open_click, self.btn_open)
        self.Bind(wx.EVT_MENU, self.__on_btn_motion_blur_click,
                  self.btn_motion_blur)

    def __get_size(self, bmp):
        width = bmp.GetWidth()
        height = bmp.GetHeight()
        if width > height:
            factor = self.IMAGE_WIDTH/width
        else:
            factor = self.IMAGE_HEIGHT/height
        width = factor*width
        height = factor*height
        return width, height

    def refresh_image(self):
        array = self.function.current_image
        shape = array.shape
        image = wx.Image(width=shape[1], height=shape[0])
        image.SetData(array.tostring())
        bitmap = image.ConvertToBitmap()
        size = self.__get_size(bitmap)
        bitmap = image.Scale(
            size[0], size[1], wx.IMAGE_QUALITY_BICUBIC).ConvertToBitmap()
        self.static_bmp.SetSize(size)
        self.static_bmp.SetBitmap(bitmap)

    def __on_btn_open_click(self, event):
        dialog = wx.FileDialog(self, message="打开文件", defaultDir=os.getcwd())
        if wx.ID_OK == dialog.ShowModal():
            try:
                array = self.function.open(dialog.GetPath())
                shape = array.shape
                if shape[2] == 4:
                    image = wx.Image(width=shape[1], height=shape[0])
                    image.SetData(array[:, :, 0:3].tostring())
                    image.SetAlpha(array[:, :, 3])
                else:
                    image = wx.Image(width=shape[1], height=shape[0])
                    image.SetData(array.tostring())
                bitmap = image.ConvertToBitmap()
                size = self.__get_size(bitmap)
                bitmap = image.Scale(
                    size[0], size[1], wx.IMAGE_QUALITY_BICUBIC).ConvertToBitmap()
                self.static_bmp.SetSize(size)
                self.static_bmp.SetBitmap(bitmap)
            except Exception:
                return

    def __on_btn_about_click(self, event):
        dialog = AbountDialog(self)
        dialog.Show()

    def __on_btn_motion_blur_click(self, event):
        def generic_callback():
            self.refresh_image()
        dialog = MotionBlurDialog(self, self.function, generic_callback,
                                  generic_callback, generic_callback)
        dialog.Show()

    def __init_widgets(self):

        panel = wx.Panel(self)
        panel.SetBackgroundColour("#F0F0F0")

        menubar = wx.MenuBar()

        filemenu = wx.Menu()
        self.btn_open = wx.MenuItem(filemenu, -1, "打开")
        self.btn_save = wx.MenuItem(filemenu, -1, "保存")
        self.btn_save_as = wx.MenuItem(filemenu, -1, "另存为")
        self.btn_quit = wx.MenuItem(filemenu, -1, "退出")
        filemenu.Append(self.btn_open)
        filemenu.Append(self.btn_save)
        filemenu.Append(self.btn_save_as)
        filemenu.Append(self.btn_quit)

        editmenu = wx.Menu()
        self.btn_undo = wx.MenuItem(editmenu, -1, "撤销")
        self.btn_redo = wx.MenuItem(editmenu, -1, "重做")
        editmenu.Append(self.btn_undo)
        editmenu.Append(self.btn_redo)

        filtermenu = wx.Menu()

        blurmenu = wx.Menu()
        self.btn_motion_blur = wx.MenuItem(blurmenu, -1, "运动模糊")
        self.btn_radial_blur = wx.MenuItem(blurmenu, -1, "径向模糊")
        self.btn_rotate_blur = wx.MenuItem(blurmenu, -1, "旋转模糊")
        blurmenu.Append(self.btn_motion_blur)
        blurmenu.Append(self.btn_radial_blur)
        blurmenu.Append(self.btn_rotate_blur)

        twistmenu = wx.Menu()
        self.btn_wave_twist = wx.MenuItem(twistmenu, -1, "波浪")
        twistmenu.Append(self.btn_wave_twist)

        stylemenu = wx.Menu()
        self.btn_colored_glass = wx.MenuItem(twistmenu, -1, "染色玻璃")
        self.btn_high_pass = wx.MenuItem(twistmenu, -1, "高反差保留")
        self.btn_light_edge = wx.MenuItem(twistmenu, -1, "照亮边缘")
        stylemenu.Append(self.btn_colored_glass)
        stylemenu.Append(self.btn_high_pass)
        stylemenu.Append(self.btn_light_edge)

        filtermenu.AppendSubMenu(blurmenu, "模糊")
        filtermenu.AppendSubMenu(twistmenu, "扭曲")
        filtermenu.AppendSubMenu(stylemenu, "风格化")

        helpmenu = wx.Menu()
        self.btn_about = wx.MenuItem(helpmenu, -1, "关于")
        helpmenu.Append(self.btn_about)

        menubar.Append(filemenu, "文件")
        menubar.Append(editmenu, "编辑")
        menubar.Append(filtermenu, "滤镜")
        menubar.Append(helpmenu, "关于")

        self.static_bmp = wx.StaticBitmap(
            panel, -1, wx.NullBitmap, (10, 10), (580, 580))
        self.main_layout = wx.BoxSizer(wx.VERTICAL)
        self.main_layout.Add(self.static_bmp, 0,
                             wx.ALL, 20)
        self.SetMenuBar(menubar)
        panel.SetSizer(self.main_layout)


def test_main_window():
    app = wx.App()
    win = MainWindow(None)
    win.Show()
    app.MainLoop()


if __name__ == '__main__':
    test_main_window()
