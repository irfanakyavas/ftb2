import hashlib


class Player:
    all_players = dict()

    def __init__(self, name, team):
        self.team = None
        self.name = name
        self.num_redcards = 0
        self.num_yellowcards = 0
        self.num_goals = 0
        self.num_assists = 0
        Player.all_players[hashlib.md5(self.team.team_name + self.name)] = self

    @staticmethod
    def get_or_create_player(name, team):
        if Player.all_players[hashlib.md5(team.team_name + name)] is None:
            return Player(name, team)
        return Player.all_players[hashlib.md5(team.team_name + name)]

    def to_string(self):
        return 'Player : %-17s Team : %-17s' % (self.name , self.team.team_name)
