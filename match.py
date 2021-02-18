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
