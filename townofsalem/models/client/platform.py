from enum import IntEnum

class Platform(IntEnum):
    WEB = 1
    STEAM = 2
    AS3 = 3
    ANDROID = 4
    IOS = 8
    MOBILE = 12 # 0x0000000C
    ALL = 15 # 0x0000000F