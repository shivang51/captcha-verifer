import wx


class RegisteredFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(RegisteredFrame, self).__init__(*args, **kw)
        self.main_panel = wx.Panel(self)

        self.message = self._make_static_text_(self.main_panel, "Registration Successfully Completed")

    @staticmethod
    def _make_static_text_(panel, value, size: int = 12) -> wx.StaticText:
        st = wx.StaticText(panel, label=value)
        font = st.GetFont()
        font.SetPointSize(size)
        st.SetFont(font)
        st.SetMinSize((150, -1))
        return st
