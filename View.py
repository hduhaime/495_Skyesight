import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty

from Util import OnScreenButtons
from Util import DisplaySelection

#IMAGES
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture

#TODO:
import cv2



class VideoFeed(Image):
    def __init__(self, **kwargs):
        super(VideoFeed, self).__init__(**kwargs)

    def update_feed(self, frame):
        if(not frame):
            return
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
    def __init__(self, buttonMap, **kwargs):
        super(WindowWrapper, self).__init__(**kwargs)
        #TODO: Map buttons to appropriate functions

        self.panelMap = {
            DisplaySelection.MainLeft: self.primary_full,
            DisplaySelection.Right: self.primary_split,
            DisplaySelection.Left: self.secondary_split
        }

        pass

    def makeFullScreen(self):
        pass

    def makeSplitScreen(self):
        pass

    def toggleNotifications(self):
        pass

    def updatePanel(self, displaySelection, image):
        #TODO: Labels
        self.panelMap[displaySelection].video.update_feed(image)

    def on_stop(self):
        #TODO: Callback
        pass

class viewApp(App):

    def __init__(self, buttonMap, **kwargs):
        super(viewApp, self).__init__(**kwargs)
        self._buttonMap = buttonMap
        self.fxns = None

    def build(self):
        self.fxns = WindowWrapper(self._buttonMap)
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
    pass


# import tkinter as tki
#
# from Util import OnScreenButtons
# from Util import DisplaySelection
#
# class View:
#     def __init__(self, root, buttonMap):
#         self.root = root
#         self.buttonMap = buttonMap
#         self.panelMap = {DisplaySelection.MainLeft: None, DisplaySelection.Right: None}
#
#         # set geometry of root window
#         self.root.geometry('800x600')
#         for i in range(12):
#             self.root.grid_columnconfigure(i, weight=1)
#
#         self.root.grid_rowconfigure(0, weight=2)
#         self.root.grid_rowconfigure(1, weight=1)
#         self.root.grid_rowconfigure(2, weight=1)
#
#         # create fullscreen view
#         self.makeFullScreen()
#
#     def makeSplitScreen(self):
#         # update screen toggle button's text
#         self.buttonMap[OnScreenButtons.FullSplitscreenToggle].config(text="Make Fullscreen")
#
#         # remove fullscreen things
#         self.panelMap[DisplaySelection.MainLeft].grid_forget()
#         self.buttonMap[OnScreenButtons.MainLeftPrevFeed].grid_forget()
#         self.buttonMap[OnScreenButtons.MainLeftPrevFeed].grid_forget()
#
#         # configure buttons
#         self.buttonMap[OnScreenButtons.MainLeftPrevFeed].grid(row=1, column=1, columnspan=2, sticky="nesw")
#         self.buttonMap[OnScreenButtons.MainLeftNextFeed].grid(row=1, column=3, columnspan=2, sticky="nesw")
#         self.buttonMap[OnScreenButtons.RightPrevFeed].grid(row=1, column=7, columnspan=2, sticky="nesw")
#         self.buttonMap[OnScreenButtons.RightNextFeed].grid(row=1, column=9, columnspan=2, sticky="nesw")
#
#         # put video panels on screen
#         if self.panelMap[DisplaySelection.Right] is None:
#             self.panelMap[DisplaySelection.Right] = tki.Label(image=None, width=400, height=300)
#             self.panelMap[DisplaySelection.Right].image = None
#         self.panelMap[DisplaySelection.MainLeft].grid(row=0, columnspan=6)
#         self.panelMap[DisplaySelection.MainLeft].configure(width=400, height=300)
#         self.panelMap[DisplaySelection.Right].grid(row=0, column=6, columnspan=6)
#         self.panelMap[DisplaySelection.Right].configure(width=400, height=300)
#
#     def makeFullScreen(self):
#         # remove splitscreen buttons
#         self.buttonMap[OnScreenButtons.RightPrevFeed].grid_forget()
#         self.buttonMap[OnScreenButtons.RightNextFeed].grid_forget()
#
#         # update screen toggle button's text
#         self.buttonMap[OnScreenButtons.FullSplitscreenToggle].config(text="Make Splitscreen")
#
#         # remove splitscreen things from the window
#         if self.panelMap[DisplaySelection.Right] is not None:
#             self.panelMap[DisplaySelection.MainLeft].grid_forget()
#             self.panelMap[DisplaySelection.Right].grid_forget()
#             self.buttonMap[OnScreenButtons.MainLeftPrevFeed].grid_forget()
#             self.buttonMap[OnScreenButtons.MainLeftNextFeed].grid_forget()
#             self.buttonMap[OnScreenButtons.RightPrevFeed].grid_forget()
#             self.buttonMap[OnScreenButtons.RightNextFeed].grid_forget()
#
#         # reconfigure fullscreen buttons
#         self.buttonMap[OnScreenButtons.FullSplitscreenToggle].grid(row=2, column=0, columnspan=4, sticky='nesw')
#         self.buttonMap[OnScreenButtons.Recalibrate].grid(row=2, column=4, columnspan=4, sticky='nesw')
#         self.buttonMap[OnScreenButtons.ToggleNotifications].grid(row=2, column=8, columnspan=4, sticky='nesw')
#         self.buttonMap[OnScreenButtons.MainLeftPrevFeed].grid(row=1, column=4, columnspan=2, sticky='nesw')
#         self.buttonMap[OnScreenButtons.MainLeftNextFeed].grid(row=1, column=6, columnspan=2, sticky='nesw')
#
#         # put video panel on screen
#         if self.panelMap[DisplaySelection.MainLeft] is None:
#             self.panelMap[DisplaySelection.MainLeft] = tki.Label(image=None, width=400, height=300)
#         self.panelMap[DisplaySelection.MainLeft].grid(row=0, column=2, columnspan=8)
#         self.panelMap[DisplaySelection.MainLeft].image = None
#
#     def toggleNotifications(self, notificationsMuted):
#         if notificationsMuted:
#             self.buttonMap[OnScreenButtons.ToggleNotifications].config(text="Unmute Notifications")
#         else:
#             self.buttonMap[OnScreenButtons.ToggleNotifications].config(text="Mute Notifications")
#
#     def updatePanel(self, displaySelection, image):
#         self.panelMap[displaySelection].configure(image=image)
#         self.panelMap[displaySelection].image = image
