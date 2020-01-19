from enum import IntEnum

class LoginType(IntEnum):
    FBWeb = 1
    Web = 2
    SteamUsernamePassword = 3
    SteamIdAndAuthTicket = 4
    Mobile = 6
    FBMobile = 7