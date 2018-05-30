from window.window import MainWindow
import wx
from function import Function

if __name__ == '__main__':
    app = wx.App()
    win = MainWindow(Function())
    win.Show()
    app.MainLoop()
    