#!/usr/bin/env python
# coding=utf-8
import wx
from window.average_filter_dialog import AverageFilterDialog
from window.blur_glass_dialog import BlurGlassDialog
from window.guassian_filter_dialog import GuassianFilterDialog
from window.about_dialog import AbountDialog
from window.high_pass_dialog import HighPassDialog
from window.lighten_edge_dialog import LightenEdgeDialog
from window.median_filter_dialog import MedianFilterDialog
from window.guided_filter_dialog import SurfaceBlurDialog
from window.motion_blur_dialog import MotionBlurDialog
from function import Function
import os
import traceback

from window.wave_dialog import WaveDialog


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
        self.Bind(wx.EVT_MENU, self.__on_btn_average_filter_click,
                  self.btn_average_filter)
        self.Bind(wx.EVT_MENU, self.__on_btn_guassian_filter_click,
                  self.btn_guassian_filter)
        self.Bind(wx.EVT_MENU, self.__on_btn_median_filter_click,
                  self.btn_median_filter)
        self.Bind(wx.EVT_MENU, self.__on_btn_surface_blur_click,
                  self.btn_surface_blur)
        self.Bind(wx.EVT_MENU, self.__on_btn_wave_click,
                  self.btn_wave_twist)
        self.Bind(wx.EVT_MENU, self.__on_btn_high_pass_click,
                  self.btn_high_pass)
        self.Bind(wx.EVT_MENU, self.__on_btn_lighten_edge_click,
                  self.btn_light_edge)
        self.Bind(wx.EVT_MENU, self.__on_btn_blur_glass_click,
                  self.btn_blur_glass)
        self.Bind(wx.EVT_MENU, self.__on_btn_undo_click, self.btn_undo)
        self.Bind(wx.EVT_MENU, self.__on_btn_redo_click, self.btn_redo)

    def __on_btn_save_click(self, evt):
        try:
            self.function.save()
        except:
            traceback.print_exc()

    def __on_btn_save_as_click(self, evt):
        dialog = wx.FileDialog(self, message="保存图片", defaultDir=os.getcwd())
        if wx.OK == dialog.ShowModal():
            try:
                self.function.save(dialog.GetPath())
            except:
                traceback.print_exc()

    def __on_btn_redo_click(self, event):
        self.function.redo()
        self.refresh_image()

    def __on_btn_undo_click(self, event):
        self.function.undo()
        self.refresh_image()

    def __get_size(self, bmp):
        width = bmp.GetWidth()
        height = bmp.GetHeight()
        if width > height:
            factor = self.IMAGE_WIDTH / width
        else:
            factor = self.IMAGE_HEIGHT / height
        width = factor * width
        height = factor * height
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

    def __on_btn_motion_blur_click(self, evt):
        self.__on_btn_img_process_click(MotionBlurDialog)

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

    def __on_btn_img_process_click(self, dialog_cls):
        def generic_callback():
            self.refresh_image()

        dialog = dialog_cls(self, self.function, generic_callback,
                            generic_callback, generic_callback)
        dialog.Show()

    def __on_btn_average_filter_click(self, event):
        self.__on_btn_img_process_click(AverageFilterDialog)

    def __on_btn_guassian_filter_click(self, evt):
        self.__on_btn_img_process_click(GuassianFilterDialog)

    def __on_btn_median_filter_click(self, evt):
        self.__on_btn_img_process_click(MedianFilterDialog)

    def __on_btn_surface_blur_click(self, evt):
        self.__on_btn_img_process_click(SurfaceBlurDialog)

    def __on_btn_wave_click(self, evt):
        self.__on_btn_img_process_click(WaveDialog)

    def __on_btn_high_pass_click(self, evt):
        self.__on_btn_img_process_click(HighPassDialog)

    def __on_btn_lighten_edge_click(self, evt):
        self.__on_btn_img_process_click(LightenEdgeDialog)

    def __on_btn_blur_glass_click(self, evt):
        self.__on_btn_img_process_click(BlurGlassDialog)

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
        self.btn_average_filter = wx.MenuItem(blurmenu, -1, "均值滤波")
        self.btn_median_filter = wx.MenuItem(blurmenu, -1, "中值滤波")
        self.btn_guassian_filter = wx.MenuItem(blurmenu, -1, "高斯滤波")
        self.btn_surface_blur = wx.MenuItem(blurmenu, -1, "导向滤波")
        blurmenu.Append(self.btn_motion_blur)
        blurmenu.Append(self.btn_average_filter)
        blurmenu.Append(self.btn_median_filter)
        blurmenu.Append(self.btn_guassian_filter)
        blurmenu.Append(self.btn_surface_blur)

        twistmenu = wx.Menu()
        self.btn_wave_twist = wx.MenuItem(twistmenu, -1, "波浪")
        twistmenu.Append(self.btn_wave_twist)

        stylemenu = wx.Menu()
        self.btn_high_pass = wx.MenuItem(twistmenu, -1, "高反差保留")
        self.btn_light_edge = wx.MenuItem(twistmenu, -1, "照亮边缘")
        self.btn_blur_glass = wx.MenuItem(twistmenu, -1, "模糊玻璃")
        stylemenu.Append(self.btn_high_pass)
        stylemenu.Append(self.btn_light_edge)
        stylemenu.Append(self.btn_blur_glass)

        filtermenu.AppendSubMenu(blurmenu, "模糊")
        filtermenu.AppendSubMenu(twistmenu, "扭曲")
        filtermenu.AppendSubMenu(stylemenu, "特效")

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
