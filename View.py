import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty

from Util import OnScreenButtons
from Util import DisplaySelection, VideoSelection, CamList

import threading

#IMAGES
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.popup import Popup

#TODO:
import cv2

VIEW_ROOT = None

COLOR = False

class DistanceNotification(Popup):
    def __init__(self, camType, distance, label, **kwargs):
        super(DistanceNotification, self).__init__(**kwargs)

        self.distance_lock = threading.Lock()
        self.popup_lock = threading.Lock()

        self.camText.text = "Object detected by " + label + "-facing camera"

        self.prefix = "Distance: "
        self.camType = camType
        self.update_distance(distance)

    def update_distance(self, distance):
        self.distance_lock.acquire()
        self.distance = distance
        self.distText.text = self.prefix + str(distance) + "m"
        self.distance_lock.release()

    def click_dismiss(self):

        self.popup_lock.acquire()
        VIEW_ROOT.popup = None
        self.dismiss()
        self.popup_lock.release()

        VIEW_ROOT.registerButtonPressArgument("onDismissNotification", self.camType)
        pass

    def click_goto_feed(self):

        self.popup_lock.acquire()
        VIEW_ROOT.popup = None
        self.dismiss()
        self.popup_lock.release()

        VIEW_ROOT.registerButtonPressArgument("onGotoNotification", self.camType)
        pass


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

        fmt = 'bgr' if COLOR else 'luminance'

        image_texture = Texture.create(
            size=(next_frame_shape[1], next_frame_shape[0]), colorfmt=fmt)
        image_texture.blit_buffer(buf, colorfmt=fmt, bufferfmt='ubyte')

        self.texture = image_texture

    def update_feed(self, frame, color, text):
        self.feed_lock.acquire()
        self.next_frame = frame
        self.next_text = text
        global COLOR
        COLOR = color
        self.feed_lock.release()
        return

class Toolbar (BoxLayout):
    def __init__(self, **kwargs):
        super(Toolbar, self).__init__(**kwargs)
        self.oldvalue = 1.5


    def click_toggle_screen(self):
        VIEW_ROOT.registerButtonPress("onToggleScreen")

    def click_recalibrate(self):
        VIEW_ROOT.registerButtonPress("onRecalibrate")

    def click_toggle_notifications(self):
        VIEW_ROOT.registerButtonPress("onToggleNotifications")

    def on_slider_value_change(self, value):
        if self.oldvalue != value:
            self.oldvalue = value

            VIEW_ROOT.registerButtonPressArgument("onChangeDistanceRange", value)




class WindowWrapper(BoxLayout):
    def __init__(self, buttonMap, buttonMapArgs, **kwargs):
        super(WindowWrapper, self).__init__(**kwargs)

        self.panelMap = {
            VideoSelection.Main: self.primary_full,
            VideoSelection.Left: self.primary_split,
            VideoSelection.Right: self.secondary_split
        }

        self._buttonMap = buttonMap
        self._buttonMapArgs = buttonMapArgs
        self.popup = None


    def registerButtonPress(self, eventName):
        self._buttonMap[eventName]()

    def registerButtonPressArgument(self, eventName, argument):
        self._buttonMapArgs[eventName](argument)

    def makeFullScreen(self):
        self.manager.transition.direction = "right"
        self.manager.current = "FULLSCREEN"

    def makeSplitScreen(self):
        self.manager.transition.direction = "left"
        self.manager.current = "SPLITSCREEN"

    def toggleNotifications(self, muted):
        #TODO:
        pass

    def updatePanel(self, videoSelection, image, color, text):
        self.panelMap[videoSelection].video.update_feed(image, color, text)

    def sendDistanceNotification(self, camType, distance, feedTitle):

        if self.popup is None:
            self.popup = DistanceNotification(camType, distance, feedTitle)
            self.popup.popup_lock.acquire()
            self.popup.open()
            self.popup.popup_lock.release()
        else:
            self.popup.popup_lock.acquire()
            if (camType == self.popup.camType):
                self.popup.update_distance(distance)
            self.popup.popup_lock.release()

        # print(str(self.popup.isOpen) + " " + feedTitle)


class viewApp(App):

    def __init__(self, **kwargs):
        super(viewApp, self).__init__(**kwargs)
        self.fxns = None
        self._buttonMap = None

    def initialize(self, buttonMap, buttonMapArgs):
        self._buttonMap = buttonMap
        self._buttonMapArgs = buttonMapArgs

    def build(self):
        global VIEW_ROOT
        self.fxns = WindowWrapper(self._buttonMap, self._buttonMapArgs)
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

