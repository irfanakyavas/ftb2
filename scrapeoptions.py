from enum import Enum


class League(Enum):
    EN_PREMIER_LEAGUE = ("england", "premier-league")
    TR_SUPER_LEAGUE = ("turkey", "super-lig")

class DriverType(Enum):
    FIREFOX = 1
    CHROME = 2
    OPERA = 3
