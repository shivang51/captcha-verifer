from captcha.image import ImageCaptcha
from captcha.audio import AudioCaptcha
import wx
import random
import sounddevice as sd


class Captcha:
    def __init__(self):
        self._image_captcha_ = ImageCaptcha()
        self._audio_captcha_ = AudioCaptcha()
        self._value_ = ""

    def generate(self, text: str) -> any:
        img = self._image_captcha_.generate_image(text)
        width, height = img.size
        return wx.Bitmap.FromBuffer(width, height, img.tobytes())

    def random(self):
        self._value_ = str(random.randrange(1001, 9999))
        img = self._image_captcha_.generate_image(self._value_)
        width, height = img.size
        return wx.Bitmap.FromBuffer(width, height, img.tobytes())

    def verify(self, value: str):
        return self._value_ == value

    def play(self):
        raw_audio = self._audio_captcha_.generate(self._value_)
        sd.play(raw_audio, 8000)
