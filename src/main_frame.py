import wx
import os
from PIL import Image
import re
from m_captcha import Captcha
import numpy as np

from registered_frame import RegisteredFrame


class MainFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw)

        self.registered_frame = RegisteredFrame(None, title="Registered Successfully")

        self._tb_data_ = {
            "name": "",
            "email": "",
            "password": "",
            "c_password": "",
            "captcha": ""
        }

        self._color_red_ = (255, 0, 0, 255)
        self._color_green_ = (0, 155, 0, 255)

        self._captcha_ = Captcha()

        self.image_captcha_sizer = None
        self.image_captcha = None
        self.SetMinSize((700, 500))

        self._init_assets_()
        self._init_ui_()

        self._bind_events_()

    def __del__(self):
        self.registered_frame.Destroy()

    def _bind_events_(self):
        self.Bind(wx.EVT_BUTTON, self.on_submit_click, self.button_submit)
        self.Bind(wx.EVT_BUTTON, self.on_refresh_captcha_click, self.button_refresh_captcha)
        self.tb_name.Bind(wx.EVT_TEXT, self.on_input_name_change)
        self.tb_email.Bind(wx.EVT_TEXT, self.on_input_email_change)
        self.tb_password.Bind(wx.EVT_TEXT, self.on_input_password_change)
        self.tb_c_password.Bind(wx.EVT_TEXT, self.on_input_c_password_change)

    def _init_assets_(self):
        self._assets_ = {
            "refresh_icon_64x64":  os.path.join("../assets/images", "icons-refresh-64.png")
        }

    def _init_ui_(self):
        self.main_panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self._init_ui_elements_(self.main_panel)
        self._assemble_ui_elements_()
        self.main_panel.SetSizer(self.main_sizer)

    def _init_ui_elements_(self, panel) -> None:
        """
        Internal Method
        Initializes elements of UI
        :parameter panel: panel into which these elements will belong
        :return: None
        """

        # submit Heading
        self.heading_submit = self._make_static_text_(panel, "Register", 24)

        # ============= User Name Input ===================
        self.label_name = self._make_static_text_(panel, "Name")
        self.label_warn_name = self._create_warn_label_(panel)
        self.tb_name = wx.TextCtrl(panel)
        self.tb_name.SetMinSize((250, 24))

        # ============= Email Input ===================
        self.label_email = self._make_static_text_(panel, "Email")
        self.label_warn_email = self._create_warn_label_(panel)
        self.tb_email = wx.TextCtrl(panel)
        self.tb_email.SetMinSize((250, 24))

        # ============= Password Input ===================
        self.label_password = self._make_static_text_(panel, "Password")
        self.label_warn_password = self._create_warn_label_(panel)
        self.tb_password = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        self.tb_password.SetMinSize((250, 24))

        # ============= Confirm-Password Input ===================
        self.label_c_password = self._make_static_text_(panel, "Confirm Password")
        self.label_warn_c_password = self._create_warn_label_(panel)
        self.tb_c_password = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        self.tb_c_password.SetMinSize((250, 24))

        # ============= Captcha Refresh Button ======
        png = self._png_to_bitmap_(self._assets_["refresh_icon_64x64"], size=(24, 24))
        self.button_refresh_captcha = wx.BitmapButton(panel, -1, png)

        # ============= Captcha Image ===============
        png = self._captcha_.random()
        self.image_captcha = wx.StaticBitmap(panel, -1, png)

        # ============= Captcha Input ===============
        self.label_captcha = self._make_static_text_(panel, "Enter Code")
        self.label_warn_captcha = self._create_warn_label_(panel)
        self.tb_captcha = wx.TextCtrl(panel)
        self.tb_captcha.SetMinSize((250, 24))

        # ============= Submit Button ================
        self.button_submit = wx.Button(panel, label='Submit', size=(70, 26))
        self.button_submit.Disable()
        self.label_warn_submit = self._create_warn_label_(panel)

    def _assemble_ui_elements_(self) -> None:
        """
        Internal Method
        Assembles initialized UI elements into UI structure
        :return: None
        """

        # ======================= submit Heading ============================
        self.main_sizer.Add(self.heading_submit, flag=wx.LEFT | wx.TOP | wx.CENTER, border=10)
        self.main_sizer.Add((-1, 10))

        # ____________ Inputs _______________

        # ======================= submit Input ============================
        self.submit_input = self._assemble_label_tb(self.label_name, self.tb_name, self.label_warn_name)
        self.main_sizer.Add(self.submit_input, flag=wx.CENTER | wx.TOP, border=10)

        # ======================= Email Input ============================
        self.email_input = self._assemble_label_tb(self.label_email, self.tb_email, self.label_warn_email)
        self.main_sizer.Add(self.email_input, flag=wx.CENTER | wx.TOP, border=10)

        # ======================= Password Input ============================
        self.password_input = self._assemble_label_tb(self.label_password, self.tb_password, self.label_warn_password)
        self.main_sizer.Add(self.password_input, flag=wx.CENTER | wx.TOP, border=10)

        # ======================= Confirm Password Input ============================
        self.c_password_input = self._assemble_label_tb(self.label_c_password, self.tb_c_password,
                                                        self.label_warn_c_password)
        self.main_sizer.Add(self.c_password_input, flag=wx.CENTER | wx.TOP, border=10)

        self.main_sizer.Add((-1, 40))

        # ___________________________________

        # ======================= Captcha Image ============================
        self.image_captcha_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.image_captcha_sizer.Add(self.button_refresh_captcha, flag=wx.ALIGN_BOTTOM | wx.LEFT)
        self.image_captcha_sizer.Add((5, -1))
        self.image_captcha_sizer.Add(self.image_captcha, flag=wx.RIGHT)
        self.main_sizer.Add(self.image_captcha_sizer, flag=wx.CENTER | wx.BOTTOM, border=10)

        # ======================= Captcha Input ============================
        self.captcha_input = self._assemble_label_tb(self.label_captcha, self.tb_captcha, self.label_warn_captcha)
        self.main_sizer.Add(self.captcha_input, flag=wx.CENTER | wx.BOTTOM, border=10)
        self.main_sizer.Add((-1, 10))

        # ======================= Submit Button ==============================
        self.submit_area = wx.BoxSizer(wx.HORIZONTAL)
        self.submit_area.Add(self.button_submit, flag=wx.RIGHT, border=10)
        self.submit_area.Add(self.label_warn_submit, flag=wx.LEFT, border=10)
        self.main_sizer.Add(self.submit_area, flag=wx.ALIGN_CENTER)
        self.main_sizer.Add((-1, 10))

    def on_input_name_change(self, _):
        value = self.tb_name.GetValue()
        self._tb_data_["name"] = value
        self.label_warn_name.SetLabel("")

    def on_input_email_change(self, _):
        value = self.tb_email.GetValue()
        self._tb_data_["email"] = value

        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        if value == "":
            self.label_warn_email.SetLabel("")
            self.button_submit.Enable()
        elif not re.fullmatch(pattern, value):
            self.label_warn_email.SetForegroundColour(self._color_red_)
            self.label_warn_email.SetLabel("Invalid Email")
            self.button_submit.Disable()
        else:
            self.label_warn_email.SetForegroundColour(self._color_green_)
            self.label_warn_email.SetLabel("Email Verified")
            self.button_submit.Enable()

    def on_input_password_change(self, _):
        value = self.tb_password.GetValue()
        self._tb_data_["password"] = value

        if value == "" or len(value) >= 6:
            self.label_warn_password.SetLabel("")
            self.button_submit.Enable()
        elif len(value) < 6:
            self.label_warn_password.SetLabel("Minimum length should be 6")
            self.button_submit.Disable()

    def on_input_c_password_change(self, _):
        value = self.tb_c_password.GetValue()
        self._tb_data_["c_password"] = value

        if value == "":
            self.label_warn_c_password.SetLabel("")
            self.button_submit.Enable()
        elif value == self._tb_data_["password"]:
            self.label_warn_c_password.SetForegroundColour(self._color_green_)
            self.label_warn_c_password.SetLabel("Passwords matched")
            self.button_submit.Enable()
        else:
            self.label_warn_c_password.SetForegroundColour(self._color_red_)
            self.label_warn_c_password.SetLabel("Passwords do not match")
            self.button_submit.Disable()

    def on_input_captcha_change(self, _):
        value = self.tb_captcha.GetValue()
        self._tb_data_["captcha"] = value

    def on_submit_click(self, _):
        success = True
        if self.tb_name.GetValue() == "":
            success = False
            self.label_warn_name.SetLabel("Can not be empty")
        if self.tb_email.GetValue() == "":
            success = False
            self.label_warn_email.SetLabel("Can not be empty")
        if self.tb_password.GetValue() == "":
            success = False
            self.label_warn_password.SetLabel("Can not be empty")
        if self.tb_captcha.GetValue() == "":
            success = False
            self.label_warn_captcha.SetLabel("Can not be empty")

        if not self._captcha_.verify(self.tb_captcha.GetValue()):
            success = False
            self.label_warn_captcha.SetForegroundColour(self._color_red_)
            self.label_warn_captcha.SetLabel("Captcha verification failed")
        else:
            self.label_warn_captcha.SetForegroundColour(self._color_green_)
            self.label_warn_captcha.SetLabel("Verified")

        if not success:
            self.label_warn_submit.SetForegroundColour(self._color_red_)
            self.label_warn_submit.SetLabel("Please correct above errors!")
        else:
            self.label_warn_submit.SetForegroundColour(self._color_green_)
            self.label_warn_submit.SetLabel("Successfully Registered")
            self.registered_frame.Show()
            self.Hide()

    def on_refresh_captcha_click(self, _):
        self._refresh_captcha_()

    def _refresh_captcha_(self):
        png = self._captcha_.random()
        pos = self.image_captcha.GetPosition()
        self.image_captcha.Destroy()
        self.image_captcha = wx.StaticBitmap(self.main_panel, -1, png, pos)
        self.image_captcha_sizer.Add(self.image_captcha, flag=wx.CENTER | wx.BOTTOM, border=10)

    @staticmethod
    def _assemble_label_tb(label: wx.StaticText, tb: wx.TextCtrl, warn_label: wx.StaticText = None) -> wx.BoxSizer:
        h_box = wx.BoxSizer(wx.HORIZONTAL)
        h_box.Add(label, flag=wx.RIGHT, border=8)
        h_box.Add(tb, proportion=1, border=10)
        if warn_label:
            h_box.Add(warn_label, flag=wx.LEFT, border=8)
        return h_box

    @staticmethod
    def _make_static_text_(panel, value, size: int = 12) -> wx.StaticText:
        st = wx.StaticText(panel, label=value)
        font = st.GetFont()
        font.SetPointSize(size)
        st.SetFont(font)
        st.SetMinSize((150, -1))
        return st

    @staticmethod
    def _png_to_bitmap_(path: str, size: tuple = None) -> wx.Bitmap:
        png = Image.open(path)
        if size:
            png = png.resize(size)


        pix = np.array(png)
        font_color = wx.Button().GetForegroundColour()[:3]
    
        pix_data = np.array([[[*font_color, pix[-1]] if pix[-1] > 0 else pix for pix in row ] for row in pix], dtype=np.uint8)


        png = Image.fromarray(pix)

        bg = wx.Button().GetBackgroundColour()
        bg = bg[:3]

        img = Image.new("RGB", png.size, bg)
        img.paste(png, mask=png.split()[3])

        width, height = img.size
        return wx.Bitmap.FromBuffer(width, height, img.tobytes())

    def _create_warn_label_(self, panel: wx.Panel) -> wx.StaticText:
        label = self._make_static_text_(panel, "")
        label.SetForegroundColour((255, 0, 0, 255))
        label.SetMinSize((200, 24))
        return label
