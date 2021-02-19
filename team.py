from mongoengine import *


class TeamDocument(Document):
    team_name = StringField(required=True)


class Team:

    all_teams = {}

    def __init__(self, team_name):
        self.team_name = team_name
        self.matches = []

    @staticmethod
    def get_or_create_team(team_name):
        if Team.all_teams.get(team_name) is (False or None):
            return Team(team_name)
        return Team.all_teams.get(team_name)

    def to_string(self):
        return 'Team Name : %25s' % (self.team_name)
