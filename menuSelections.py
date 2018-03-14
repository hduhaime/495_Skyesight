from graphics import LayoutSettings, FeedList
import tkinter as tki

class LayoutMenu:
    def __init__(self, application):
        self.parentApp = application
        self.window = tki.Toplevel()
        self.fullScreenBt = tki.Button(self.window, text="Fullscreen", command=self.switch_to_fullscreen)
        self.fullScreenBt.pack()
        self.splitScreenBt = tki.Button(self.window, text="Splitscreen", command=self.switch_to_splitscreen)
        self.splitScreenBt.pack()

        if application.layoutSelection.value == LayoutSettings.Fullscreen.value:
            self.fullScreenBt.config(relief="sunken")
        else:
            self.splitScreenBt.config(relief="sunken")

    def switch_to_fullscreen(self):
        if self.parentApp.layoutSelection == LayoutSettings.Fullscreen:
            self.window.destroy()
            return

        self.fullScreenBt.config(relief="sunken")
        self.splitScreenBt.config(relief="raised")
        self.parentApp.layoutSelection = LayoutSettings.Fullscreen
        self.window.destroy()


    def switch_to_splitscreen(self):
        if self.parentApp.layoutSelection == LayoutSettings.Splitscreen:
            self.window.destroy()
            return

        self.splitScreenBt.config(relief="sunken")
        self.fullScreenBt.config(relief="raised")
        self.parentApp.layoutSelection = LayoutSettings.Splitscreen
        self.window.destroy()


class FeedMenu:
    def __init__(self, application):
        self.parentApp = application
        self.buttonList = []
        self.window = tki.Toplevel()

        self.buttonList.append(tki.Button(self.window, text="Overhead",
                                          command=lambda: self.select_feed(FeedList.Overhead)))
        self.buttonList.append(tki.Button(self.window, text="Single - Left",
                                          command=lambda: self.select_feed(FeedList.SingleLeft)))
        self.buttonList.append(tki.Button(self.window, text="Single - Rear",
                                          command=lambda: self.select_feed(FeedList.SingleRear)))
        self.buttonList.append(tki.Button(self.window, text="Single - Right",
                                          command=lambda: self.select_feed(FeedList.SingleRight)))
        self.buttonList.append(tki.Button(self.window, text="Dual - Left/Rear",
                                          command=lambda: self.select_feed(FeedList.DualLR)))
        self.buttonList.append(tki.Button(self.window, text="Dual - Right/Rear",
                                          command=lambda: self.select_feed(FeedList.DualRR)))

        for button in self.buttonList:
            button.pack()

        self.buttonList[self.parentApp.feedSelection.value].config(relief="sunken")


    def select_feed(self, feedSelection):
        if self.parentApp.feedSelection.value == feedSelection.value:
            self.window.destroy()
            return

        self.buttonList[feedSelection.value].config(relief="sunken")
        self.buttonList[self.parentApp.feedSelection.value].config(relief="raised")

        self.parentApp.feedSelection = feedSelection

        self.window.destroy()
