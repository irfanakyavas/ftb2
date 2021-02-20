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

    def __str__(self):
        s = '-------------------------------\nTeam Name : %25s\nMatches:\n' % (self.team_name)
        for match in self.matches:
            s = s + match.__str__() + "\n"
        return s
