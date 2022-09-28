import wx
from main_frame import MainFrame

if __name__ == "__main__":
    app = wx.App()
    frm = MainFrame(None, title='Captcha Verifier')
    frm.Show()
    app.MainLoop()
