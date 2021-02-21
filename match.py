import json
from enum import Enum
from typing import List
from team import Team


class MatchResult(Enum):
    AWAY_WIN = -1
    DRAW = 0
    HOME_WIN = 1


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
        self.match_result = 0
        self.home_team_lineup = []
        self.away_team_lineup = []

    def __str__(self):
        s = ""
        for num in range(0, 11):
            s = s + "%-18s \t %-18s \n" % (self.home_team_lineup[num], self.away_team_lineup[num])
        return Match.line_seperator + f'{self.home_team.team_name} vs. {self.away_team.team_name} ({self.scores[0]}-{self.scores[1]})\n' + s + "-----------------------------------\n"

    def lineups_to_json(self):
        return [json.dumps(self.home_team_lineup), json.dumps(self.away_team_lineup)]

    @staticmethod
    def from_data(scores: List[int], home_team_name: str, away_team_name: str, ball_possession: List[int],
                  goal_attempts: List[int],shots_on_goal: List[int], shots_off_goal: List[int], blocked_shots: List[int],
                  free_kicks: List[int], corner_kicks: List[int], offsides: List[int], goalkeeper_saves: List[int],
                  fouls: List[int], yellow_cards: List[int], red_cards: List[int], total_passes: List[int],
                  tackles: List[int], attacks: List[int], dangerous_attacks: List[int], match_result: int,
                  home_team_lineup_json: str, away_team_lineup_json: str):
        home_team = Team.get_or_create_team(home_team_name)
        away_team = Team.get_or_create_team(away_team_name)
        home_team_lineup = json.loads(home_team_lineup_json)
        away_team_lineup = json.loads(away_team_lineup_json)

        return Match(scores, home_team, away_team, ball_possession, goal_attempts, shots_on_goal, shots_off_goal, blocked_shots,
                     free_kicks, corner_kicks, offsides, goalkeeper_saves, fouls, yellow_cards, red_cards, total_passes,
                     tackles, attacks, dangerous_attacks, match_result, home_team_lineup, away_team_lineup)
