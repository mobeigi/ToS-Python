from .items import *

RS = b'\x1E' # Record Seperator ASCII Code 30
NULL = b'\x00'
COMMA = b'\x2C'

class Currency(IntEnum):
    TOWN_POINTS = 1
    STEAM_WALLET = 2
    MERIT_POINTS = 3