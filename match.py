class Match:

    def __init__(self, home_team, away_team, no, league):
        self.home_team = home_team
        self.away_team = away_team
        self.no = no
        self.league = league

    def to_string(self):
        return '%-8s Match #%2d  %-18s vs.  %-18s' % (self.league, self.no, self.home_team.team_name, self.away_team.team_name)
