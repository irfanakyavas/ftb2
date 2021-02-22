import hashlib

from team import Team


class Player:
    all_players = {}

    def __init__(self, player_team_name, player_name):
        self.player_team_name = player_team_name
        self.player_name = player_name
        self.player_id = 0
        self.player_team_id = 0
        self.attributes = {'player_attack': 0, 'player_skill': 0, 'player_movement': 0, 'player_power': 0, 'player_mentality': 0, 'player_defending': 0}
        Player.all_players[self.md5(player_team_name, player_name)] = self

    @staticmethod
    def get_or_create_player(player_team_name, player_name):
        if Player.all_players.get(Player.md5(player_team_name, player_name)) is None:
            return Player(player_team_name, player_name)
        return Player.all_players.get(Player.md5(player_team_name, player_name))

    def get_team(self):
        return Team.all_teams.get(self.player_team_name)

    def __str__(self):
        return 'Player: %15s, Team: %15s' % (self.player_name, self.player_team_name)

    @staticmethod
    def md5(player_team_name, player_name):
        return hashlib.md5((player_team_name + player_name).encode('utf-8'))
