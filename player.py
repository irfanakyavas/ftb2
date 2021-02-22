from team import Team
import hashlib


class Player:
    all_players = {}

    def __init__(self, player_team_name, player_name):
        self.player_team_name = player_team_name
        self.player_name = player_name
        Player.all_players[self.md5(player_team_name, player_name)] = self

    @staticmethod
    def get_or_create_player(player_team_name, player_name):
        if Player.all_players.get(Player.md5(player_team_name, player_name)) is None:
            return Player(player_name, player_team_name)
        return Player.all_players.get(Player.md5(player_team_name, player_name))

    def get_team(self):
        return Team.all_teams.get(self.player_team_name)

    def __str__(self):
        return 'Player: %15s, Team: %15s' % (self.player_name, self.player_team_name)

    @staticmethod
    def md5(player_team_name, player_name):
        return hashlib.md5(player_team_name + player_name)
