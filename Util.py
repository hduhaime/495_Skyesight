from enum import Enum

class VideoSelection(Enum):
    Main = 0
    Left = 1
    Right = 2

class DisplaySelection(Enum):
    MainLeft = 0
    Right = 1

class OnScreenButtons(Enum):
    FullSplitscreenToggle = 0
    Recalibrate = 1
    ToggleNotifications = 2
    MainLeftPrevFeed = 3
    MainLeftNextFeed = 4
    RightPrevFeed = 5
    RightNextFeed = 6

class CamList(Enum):
    Left = 0
    Right = 1
    Rear = 2

camToNameMap = {CamList.Left: "left", CamList.Right: "right", CamList.Rear: "rear"}

class GPIO(Enum):
    TRIG = 0
    ECHO = 1


