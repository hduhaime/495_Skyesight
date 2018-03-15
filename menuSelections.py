from graphics import LayoutSettings, FeedList
import tkinter as tki

class LayoutMenu:
    def __init__(self, application):
        self.parentApp = application
        self.window = tki.Toplevel()
        self.window.state("zoomed")
        self.fullScreenBt = tki.Button(self.window, text="Fullscreen", command=self.switch_to_fullscreen)
        self.fullScreenBt.pack(fill='both', expand=True)
        self.splitScreenBt = tki.Button(self.window, text="Splitscreen", command=self.switch_to_splitscreen)
        self.splitScreenBt.pack(fill='both', expand=True)

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
        self.parentApp.switch_to_fullscreen()
        self.window.destroy()


    def switch_to_splitscreen(self):
        if self.parentApp.layoutSelection == LayoutSettings.Splitscreen:
            self.window.destroy()
            return

        self.splitScreenBt.config(relief="sunken")
        self.fullScreenBt.config(relief="raised")
        self.parentApp.switch_to_splitscreen()
        self.window.destroy()


class FeedMenu:
    def __init__(self, application):
        self.parentApp = application
        self.buttonList = []
        self.rhsButtonList = []
        self.window = tki.Toplevel()
        self.window.state("zoomed")

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
            button.pack(fill='both', expand=True)

        if self.parentApp.layoutSelection.value == LayoutSettings.Splitscreen.value:
            # append another set of buttons for the right hand side feed
            self.rhsButtonList.append(tki.Button(self.window, text="Overhead",
                                              command=lambda: self.select_feed(FeedList.Overhead)))
            self.rhsButtonList.append(tki.Button(self.window, text="Single - Left",
                                              command=lambda: self.select_feed(FeedList.SingleLeft)))
            self.rhsButtonList.append(tki.Button(self.window, text="Single - Rear",
                                              command=lambda: self.select_feed(FeedList.SingleRear)))
            self.rhsButtonList.append(tki.Button(self.window, text="Single - Right",
                                              command=lambda: self.select_feed(FeedList.SingleRight)))
            self.rhsButtonList.append(tki.Button(self.window, text="Dual - Left/Rear",
                                              command=lambda: self.select_feed(FeedList.DualLR)))
            self.rhsButtonList.append(tki.Button(self.window, text="Dual - Right/Rear",
                                              command=lambda: self.select_feed(FeedList.DualRR)))

            for button in self.rhsButtonList:
                button.pack(side="right")

        self.buttonList[self.parentApp.mainFeedSelection.value].config(relief="sunken")


    def select_feed(self, feedSelection, side="lhs"):
        if self.parentApp.mainFeedSelection.value == feedSelection.value:
            self.window.destroy()
            return

        self.buttonList[feedSelection.value].config(relief="sunken")
        self.buttonList[self.parentApp.mainFeedSelection.value].config(relief="raised")

        self.parentApp.mainFeedSelection = feedSelection

        self.window.destroy()
