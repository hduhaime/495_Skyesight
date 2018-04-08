import tkinter as tki

from Util import OnScreenButtons
from Util import DisplaySelection

class View:
    def __init__(self, root, buttonMap):
        self.root = root
        self.buttonMap = buttonMap
        self.panelMap = {DisplaySelection.MainLeft: None, DisplaySelection.Right: None}

        # set geometry of root window
        self.root.geometry('800x600')
        for i in range(12):
            self.root.grid_columnconfigure(i, weight=1)

        self.root.grid_rowconfigure(0, weight=2)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)

        # create fullscreen view
        self.makeFullScreen()

    def makeSplitScreen(self):
        # update screen toggle button's text
        self.buttonMap[OnScreenButtons.FullSplitscreenToggle].config(text="Make Fullscreen")

        # remove fullscreen things
        self.panelMap[DisplaySelection.MainLeft].grid_forget()
        self.buttonMap[OnScreenButtons.MainLeftPrevFeed].grid_forget()
        self.buttonMap[OnScreenButtons.MainLeftPrevFeed].grid_forget()

        # configure buttons
        self.buttonMap[OnScreenButtons.MainLeftPrevFeed].grid(row=1, column=1, columnspan=2, sticky="nesw")
        self.buttonMap[OnScreenButtons.MainLeftNextFeed].grid(row=1, column=3, columnspan=2, sticky="nesw")
        self.buttonMap[OnScreenButtons.RightPrevFeed].grid(row=1, column=7, columnspan=2, sticky="nesw")
        self.buttonMap[OnScreenButtons.RightNextFeed].grid(row=1, column=9, columnspan=2, sticky="nesw")

        # put video panels on screen
        if self.panelMap[DisplaySelection.Right] is None:
            self.panelMap[DisplaySelection.Right] = tki.Label(image=None, width=400, height=300)
            self.panelMap[DisplaySelection.Right].image = None
        self.panelMap[DisplaySelection.MainLeft].grid(row=0, columnspan=6)
        self.panelMap[DisplaySelection.MainLeft].configure(width=400, height=300)
        self.panelMap[DisplaySelection.Right].grid(row=0, column=6, columnspan=6)
        self.panelMap[DisplaySelection.Right].configure(width=400, height=300)

    def makeFullScreen(self):
        # remove splitscreen buttons
        self.buttonMap[OnScreenButtons.RightPrevFeed].grid_forget()
        self.buttonMap[OnScreenButtons.RightNextFeed].grid_forget()

        # update screen toggle button's text
        self.buttonMap[OnScreenButtons.FullSplitscreenToggle].config(text="Make Splitscreen")

        # remove splitscreen things from the window
        if self.panelMap[DisplaySelection.Right] is not None:
            self.panelMap[DisplaySelection.MainLeft].grid_forget()
            self.panelMap[DisplaySelection.Right].grid_forget()
            self.buttonMap[OnScreenButtons.MainLeftPrevFeed].grid_forget()
            self.buttonMap[OnScreenButtons.MainLeftNextFeed].grid_forget()
            self.buttonMap[OnScreenButtons.RightPrevFeed].grid_forget()
            self.buttonMap[OnScreenButtons.RightNextFeed].grid_forget()

        # reconfigure fullscreen buttons
        self.buttonMap[OnScreenButtons.FullSplitscreenToggle].grid(row=2, column=0, columnspan=4, sticky='nesw')
        self.buttonMap[OnScreenButtons.Recalibrate].grid(row=2, column=4, columnspan=4, sticky='nesw')
        self.buttonMap[OnScreenButtons.ToggleNotifications].grid(row=2, column=8, columnspan=4, sticky='nesw')
        self.buttonMap[OnScreenButtons.MainLeftPrevFeed].grid(row=1, column=4, columnspan=2, sticky='nesw')
        self.buttonMap[OnScreenButtons.MainLeftNextFeed].grid(row=1, column=6, columnspan=2, sticky='nesw')

        # put video panel on screen
        if self.panelMap[DisplaySelection.MainLeft] is None:
            self.panelMap[DisplaySelection.MainLeft] = tki.Label(image=None, width=400, height=300)
        self.panelMap[DisplaySelection.MainLeft].grid(row=0, column=2, columnspan=8)
        self.panelMap[DisplaySelection.MainLeft].image = None

    def toggleNotifications(self, notificationsMuted):
        if notificationsMuted:
            self.buttonMap[OnScreenButtons.ToggleNotifications].config(text="Unmute Notifications")
        else:
            self.buttonMap[OnScreenButtons.ToggleNotifications].config(text="Mute Notifications")

    def updatePanel(self, displaySelection, image):
        self.panelMap[displaySelection].configure(image=image)
        self.panelMap[displaySelection].image = image

    def displayNotification(self, distance):
        pass
