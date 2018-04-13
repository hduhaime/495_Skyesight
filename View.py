import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty

from Util import OnScreenButtons
from Util import DisplaySelection, VideoSelection

import threading

#IMAGES
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
#TODO:
import cv2

VIEW_ROOT = None

class VideoFeed(Image):
    def __init__(self, **kwargs):
        super(VideoFeed, self).__init__(**kwargs)
        self.next_frame = None
        self.next_text = None
        self.feed_lock = threading.Lock()
        Clock.schedule_interval(self.process_update, 1.0 / 15) #TODO: fps

    def process_update(self, dt):

        #LOCKED
        self.feed_lock.acquire()
        if self.next_frame is None:
            self.feed_lock.release()
            return
        buf1 = cv2.flip(self.next_frame, 0)

        next_frame_shape = self.next_frame.shape
        self.video_label.text = self.next_text
        self.feed_lock.release()
        #UNLOCKED

        buf = buf1.tostring()

        image_texture = Texture.create(
            size=(next_frame_shape[1], next_frame_shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

        self.texture = image_texture

    def update_feed(self, frame, text):
        self.feed_lock.acquire()
        self.next_frame = frame
        self.next_text = text
        self.feed_lock.release()
        return

class Toolbar (BoxLayout):

    def click_toggle_screen(self):
        VIEW_ROOT.registerButtonPress("onToggleScreen")

    def click_recalibrate(self):
        VIEW_ROOT.registerButtonPress("onRecalibrate")



class WindowWrapper(BoxLayout):
    def __init__(self, buttonMap, **kwargs):
        super(WindowWrapper, self).__init__(**kwargs)

        self.panelMap = {
            VideoSelection.Main: self.primary_full,
            VideoSelection.Left: self.primary_split,
            VideoSelection.Right: self.secondary_split
        }

        self._buttonMap = buttonMap

        pass

    def registerButtonPress(self, eventName):
        self._buttonMap[eventName]()

    def makeFullScreen(self):
        self.manager.transition.direction = "right"
        self.manager.current = "FULLSCREEN"

    def makeSplitScreen(self):
        self.manager.transition.direction = "left"
        self.manager.current = "SPLITSCREEN"

    def toggleNotifications(self):
        #TODO:
        pass

    def updatePanel(self, videoSelection, image, text):
        self.panelMap[videoSelection].video.update_feed(image, text)

    def on_stop(self):
        #TODO: Callback for cleanup
        pass

class viewApp(App):

    def __init__(self, **kwargs):
        super(viewApp, self).__init__(**kwargs)
        self.fxns = None
        self._buttonMap = None

    def initialize(self, buttonMap):
        self._buttonMap = buttonMap

    def build(self):
        global VIEW_ROOT
        self.fxns = WindowWrapper(self._buttonMap)
        VIEW_ROOT = self.fxns
        return self.fxns



#
#           MISC. KIVY CLASSES
#

class ScreenManagement(ScreenManager):
    pass

class FullScreenWindow(Screen):
    pass

class SplitScreenWindow(Screen):
    pass

class CamView(BoxLayout):

    def onClickPrev(self, dType):
        if(dType == DisplaySelection.MainLeft):
            VIEW_ROOT.registerButtonPress("onPrimaryPrev")
        else:
            VIEW_ROOT.registerButtonPress("onSecondaryPrev")

    def onClickNext(self, dType):
        if (dType == DisplaySelection.MainLeft):
            VIEW_ROOT.registerButtonPress("onPrimaryNext")
        else:
            VIEW_ROOT.registerButtonPress("onSecondaryNext")

