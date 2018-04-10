from enum import Enum


class DisplaySelection(Enum):
    MainLeft = 0
    Right = 1
    Left = 2


class OnScreenButtons(Enum):
    FullSplitscreenToggle = 0
    Recalibrate = 1
    ToggleNotifications = 2
    MainLeftPrevFeed = 3
    MainLeftNextFeed = 4
    RightPrevFeed = 5
    RightNextFeed = 6

