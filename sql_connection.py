import mariadb
import json

from typing import List

from match import Match
from team import Team


class SQL_Connection():
    sql_user = "admin2"
    sql_pw = "123456"
    sql_host = "127.0.0.1"
    sql_port = 3306
    sql_db = "football_data"

    def __init__(self):
        try:
            self._SQL_Connection = mariadb.connect(
                user=SQL_Connection.sql_user,
                password=SQL_Connection.sql_pw,
                host=SQL_Connection.sql_host,
                port=SQL_Connection.sql_port,
                database=SQL_Connection.sql_db
            )
            self._SQL_Connection.autocommit = False
        except mariadb.Error as e:
            raise mariadb.Error(f"Error connecting to MariaDB Platform: {e}")

    def save_match(self, match: Match):
        cursor = self._SQL_Connection.cursor()
        match_lineups_json = match.lineups_to_json()

        query = """INSERT INTO matches (home_team_name, away_team_name, home_goals, away_goals, 
        home_possession, away_possession, home_goal_attempts, away_goal_attempts, home_shots_on_goal, 
        away_shots_on_goal, home_shots_off_goal, away_shots_off_goal, home_blocked_shots, 
        away_blocked_shots, home_free_kicks, away_free_kicks, home_corner_kicks, away_corner_kicks, 
        home_offsides, away_offsides, home_goalkeeper_saves, away_goalkeeper_saves, home_fouls, 
        away_fouls, home_yellow_cards, away_yellow_cards, home_red_cards, away_red_cards, 
        home_total_passes, away_total_passes, home_tackles, away_tackles, home_attacks, 
        away_attacks, home_dangerous_attacks, away_dangerous_attacks, home_lineup, away_lineup) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

        cursor.execute(query, (match.home_team.team_name, match.away_team.team_name, match.scores[0],
                               match.scores[1], match.ball_possession[0], match.ball_possession[1],
                               match.goal_attempts[0], match.goal_attempts[1],
                               match.shots_on_goal[0], match.shots_on_goal[1], match.shots_off_goal[0],
                               match.shots_off_goal[1], match.blocked_shots[0],
                               match.blocked_shots[1], match.free_kicks[0], match.free_kicks[1],
                               match.corner_kicks[0], match.corner_kicks[1],
                               match.offsides[0], match.offsides[1], match.goalkeeper_saves[0],
                               match.goalkeeper_saves[1], match.fouls[0],
                               match.fouls[1], match.yellow_cards[0], match.yellow_cards[1],
                               match.red_cards[0], match.red_cards[1],
                               match.total_passes[0], match.total_passes[1], match.tackles[0],
                               match.tackles[1], match.attacks[0],
                               match.attacks[1], match.dangerous_attacks[0], match.dangerous_attacks[1],
                               match_lineups_json[0], match_lineups_json[1]))

        self.save_teams([match.home_team, match.away_team])
        self._SQL_Connection.commit()

    def save_matches(self, match_list: List[Match]):
        for match in match_list:
            self.save_match(match)

    def save_team(self, team: Team):
        cursor = self._SQL_Connection.cursor()
        try:
            cursor.execute("INSERT INTO teams (team_id, team_name) VALUES (?, ?)", ("NULL", team.team_name))
        except mariadb.IntegrityError as e:
            print(f"Skipping duplicate team {team.team_name}")
    def save_teams(self, team_list: List[Team]):
        for team in team_list:
            self.save_team(team)
