from enum import IntEnum

class LoginStatus(IntEnum):
    Success = 0
    Authenticating = 1
    GenericFailure = 2
    InvalidClientVersion = 3
    InvalidPlatform = 4
    InvalidUsernamePassword = 5
    FacebookIdNotRegistered = 6
    InvalidSteamId = 7
    InvalidFacebookId = 8
    InvalidFacebookToken = 9
    SteamIdInvalid = 10
    SteamAuthTicketInvalid = 11