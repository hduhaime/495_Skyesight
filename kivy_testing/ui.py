import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty

#IMAGES
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture

#TODO:
import cv2

class CamView(BoxLayout):

    pass

class VideoFeed(Image):
    def __init__(self, **kwargs):
        super(VideoFeed, self).__init__(**kwargs)

    def update_feed(self, frame):
        # convert it to texture
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        image_texture = Texture.create(
            size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display image from the texture
        self.texture = image_texture

class Toolbar (BoxLayout):

    def click_switch_screen(self, instance, value):
        if value:
            self.manager.transition.direction = "left"
            self.manager.current = "SPLITSCREEN"
        else:
            self.manager.transition.direction = "right"
            self.manager.current = "FULLSCREEN"


class WindowWrapper(BoxLayout):
    def __init__(self, **kwargs):
        super(WindowWrapper, self).__init__(**kwargs)
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0 / 15)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            self.primary_full.video.update_feed(frame)

    def on_stop(self):
        #without this, app will not exit even if the window is closed
        self.capture.release()

class ScreenManagement(ScreenManager):
    pass

class FullScreenWindow(Screen):
    pass

class SplitScreenWindow(Screen):
    pass

class uiApp(App):

    def __init__(self, **kwargs):
        super(uiApp, self).__init__(**kwargs)

    def build(self):
        return WindowWrapper()




