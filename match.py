import json

class Match:

    line_seperator = "-----------------------------------\n"
    def __init__(self, home_team, away_team):
        self.scores = [0, 0]
        self.home_team = home_team
        self.away_team = away_team
        self.ball_possession = [0, 0]
        self.goal_attempts = [0, 0]
        self.shots_on_goal = [0, 0]
        self.shots_off_goal = [0, 0]
        self.blocked_shots = [0, 0]
        self.free_kicks = [0, 0]
        self.corner_kicks = [0, 0]
        self.offsides = [0, 0]
        self.goalkeeper_saves = [0, 0]
        self.fouls = [0, 0]
        self.yellow_cards = [0, 0]
        self.red_cards = [0, 0]
        self.total_passes = [0, 0]
        self.tackles = [0, 0]
        self.attacks = [0, 0]
        self.dangerous_attacks = [0, 0]
        self.home_team_lineup = []
        self.away_team_lineup = []

    def __str__(self):
        s = ""
        for num in range(0, 11):
            s = s + "%-18s \t %-18s \n" % (self.home_team_lineup[num], self.away_team_lineup[num])
        return Match.line_seperator + f'{self.home_team.team_name} vs. {self.away_team.team_name} ({self.scores[0]}-{self.scores[1]})\n' + s + "-----------------------------------\n"

    def lineups_to_json(self):
        return [json.dumps(self.home_team_lineup), json.dumps(self.away_team_lineup)]