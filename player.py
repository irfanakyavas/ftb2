import hashlib


class Player:
    all_players = dict()

    def __init__(self, name, team):
        self.team = None
        self.name = name
        Player.all_players[hashlib.md5(self.team.team_name + self.name)] = self

    @staticmethod
    def get_or_create_player(name, team):
        if hashlib.md5(team.team_name + name) in Player.all_players is False:
            return Player(name, team)
        return hashlib.md5(team.team_name + name) in Player.all_players

    def to_string(self):
        return 'Player : %-17s Team : %-17s' % (self.name , self.team.team_name)
