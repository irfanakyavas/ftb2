from mongoengine import *
from team import TeamDocument


class MatchDocument(Document):
    home_team = ReferenceField(TeamDocument)
    away_team = ReferenceField(TeamDocument)

    home_team_lineup = ListField(max_length=11)
    away_team_lineup = ListField(max_length=11)

    scores = ListField(max_length=2)
    ball_possession = ListField(max_length=2)
    goal_attempts = ListField(max_length=2)
    shots_on_goal = ListField(max_length=2)
    shots_off_goal = ListField(max_length=2)
    blocked_shots = ListField(max_length=2)
    free_kicks = ListField(max_length=2)
    corner_kicks = ListField(max_length=2)
    offsides = ListField(max_length=2)
    goalkeeper_saves = ListField(max_length=2)
    fouls = ListField(max_length=2)
    yellow_cards = ListField(max_length=2)
    red_cards = ListField(max_length=2)
    total_passes = ListField(max_length=2)
    tackles = ListField(max_length=2)
    attacks = ListField(max_length=2)
    dangerous_attacks = ListField(max_length=2)


class Match:

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
        return f'{self.home_team.team_name} vs. {self.away_team.team_name} ({self.scores[0]}-{self.scores[1]})'
