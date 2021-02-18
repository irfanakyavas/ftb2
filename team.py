from enum import Enum

class Team:

    all_teams = {}

    def __init__(self, team_name):
        self.team_name = team_name
        self.players = []
        self.matches = []

    @staticmethod
    def get_or_create_team(team_name):
        if Team.all_teams.get(team_name) is (False or None):
            return Team(team_name)
        return Team.all_teams.get(team_name)

    def add_player(self, player):
        self.players.append(player)

    def add_players(self, players):
        for plr in players:
            self.players.append(plr)

    def to_string(self):
        return 'Team Name : %25s' % (self.team_name)
