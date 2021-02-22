from enum import Enum

class League(Enum):
    EN_PREMIER_LEAGUE = {'matches': {'country': "england", 'league_name': "premier-league", 'season': '#TODO'},
                         'players': {'league_id': "2613", 'league_name': "premier-league", 'fm_version': '21'}}
    TR_SUPER_LEAGUE = ("turkey", "super-lig")

class DriverType(Enum):
    FIREFOX = 1
    CHROME = 2
    OPERA = 3
