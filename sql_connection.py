import logging
import mariadb
from typing import List, Union
from match import *
from team import Team
from player import Player
import json
from config import ConfigHandler

DATABASE_LOGGER = logging.getLogger("[DATABASE_CONNECTION]")


class SQL_Login:

    def __init__(self, sql_user: str, sql_pw: str, sql_host: str, sql_port: int, sql_db: str):
        self.sql_user = sql_user
        self.sql_pw = sql_pw
        self.sql_host = sql_host
        self.sql_port = sql_port
        self.sql_db = sql_db

    @staticmethod
    def from_config_handler():
        return SQL_Login(ConfigHandler.database_username, ConfigHandler.database_password, ConfigHandler.database_address,
                         int(ConfigHandler.database_port), ConfigHandler.database_name)


class SQL_Connection():
    sql_instance = None
    sql_user = ""
    sql_pw = ""
    sql_host = ""
    sql_port = 0
    sql_db = ""

    team_id_map = {}

    @staticmethod
    def get_or_init_sql_connection(sql_login: Union[SQL_Login, None]):
        if SQL_Connection.sql_instance is not None:
            return SQL_Connection
        if sql_login is None:
            DATABASE_LOGGER.error("No SQL login object was received for get_or_init_sql_connection")
            raise RuntimeError("No SQL login object was received for get_or_init_sql_connection")
        else:
            return SQL_Connection(sql_login)

    def __init__(self, sql_login: SQL_Login):
        try:
            self._SQL_Connection = mariadb.connect(
                user=sql_login.sql_user,
                password=sql_login.sql_pw,
                host=sql_login.sql_host,
                port=sql_login.sql_port,
                database=sql_login.sql_db
            )
            self._SQL_Connection.autocommit = False
            SQL_Connection.sql_instance = self
        except mariadb.Error as e:
            DATABASE_LOGGER.critical(
                f"Database connection to {SQL_Connection.sql_host}:{SQL_Connection.sql_port} could not be made.")
            raise mariadb.Error(f"Error connecting to MariaDB Platform: {e}")
        else:
            DATABASE_LOGGER.info(
                f"Successfully connected to database at {SQL_Connection.sql_host}:{SQL_Connection.sql_port}.")

    def parse_matches_from_sql_cursor(self, cursor) -> List[Match]:
        return_list = []
        for (home_team_name, home_team_id, away_team_name, away_team_id, home_goals, away_goals,
             home_possession, away_possession, home_goal_attempts, away_goal_attempts, home_shots_on_goal,
             away_shots_on_goal, home_shots_off_goal, away_shots_off_goal, home_blocked_shots,
             away_blocked_shots, home_free_kicks, away_free_kicks, home_corner_kicks, away_corner_kicks,
             home_offsides, away_offsides, home_goalkeeper_saves, away_goalkeeper_saves, home_fouls,
             away_fouls, home_yellow_cards, away_yellow_cards, home_red_cards, away_red_cards,
             home_total_passes, away_total_passes, home_tackles, away_tackles, home_attacks,
             away_attacks, home_dangerous_attacks, away_dangerous_attacks, match_result, home_lineup,
             away_lineup) in cursor:
            return_list.append(Match.from_data([home_goals, away_goals],
                                               home_team_name,
                                               away_team_name,
                                               [home_possession, away_possession],
                                               [home_goal_attempts, away_goal_attempts],
                                               [home_shots_on_goal, away_shots_on_goal],
                                               [home_shots_off_goal, away_shots_off_goal],
                                               [home_blocked_shots, away_blocked_shots],
                                               [home_free_kicks, away_free_kicks],
                                               [home_corner_kicks, away_corner_kicks],
                                               [home_offsides, away_offsides],
                                               [home_goalkeeper_saves, away_goalkeeper_saves],
                                               [home_fouls, away_fouls],
                                               [home_yellow_cards, away_yellow_cards],
                                               [home_red_cards, away_red_cards],
                                               [home_total_passes, away_total_passes],
                                               [home_tackles, away_tackles],
                                               [home_attacks, away_attacks],
                                               [home_dangerous_attacks, away_dangerous_attacks],
                                               match_result, home_lineup, away_lineup))
        return return_list

    def load_team_id_map(self):
        DATABASE_LOGGER.info(f"Trying to load the team id map from database.")
        cursor = self._SQL_Connection.cursor()
        cursor.execute("SELECT * FROM teams")
        num_teams = 0
        for (team_id, team_name) in cursor:
            SQL_Connection.team_id_map[team_name] = team_id
            num_teams = num_teams + 1
        DATABASE_LOGGER.info(f"{num_teams} team-id pairs were loaded from database")

    def save_match(self, match: Match):
        DATABASE_LOGGER.info(f"Saving a match into database")
        cursor = self._SQL_Connection.cursor()
        match_lineups_json = match.lineups_to_json()

        query = """INSERT INTO matches (home_team_name, home_team_id, away_team_name, away_team_id, home_goals, away_goals, 
        home_possession, away_possession, home_goal_attempts, away_goal_attempts, home_shots_on_goal, 
        away_shots_on_goal, home_shots_off_goal, away_shots_off_goal, home_blocked_shots, 
        away_blocked_shots, home_free_kicks, away_free_kicks, home_corner_kicks, away_corner_kicks, 
        home_offsides, away_offsides, home_goalkeeper_saves, away_goalkeeper_saves, home_fouls, 
        away_fouls, home_yellow_cards, away_yellow_cards, home_red_cards, away_red_cards, 
        home_total_passes, away_total_passes, home_tackles, away_tackles, home_attacks, 
        away_attacks, home_dangerous_attacks, away_dangerous_attacks, match_result, home_lineup, away_lineup) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

        cursor.execute(query, (match.home_team.team_name, self.team_id_map[match.home_team.team_name],
                               match.away_team.team_name, self.team_id_map[match.away_team.team_name],
                               match.scores[0], match.scores[1], match.ball_possession[0], match.ball_possession[1],
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
                               match.tackles[1], match.attacks[0], match.attacks[1],
                               match.dangerous_attacks[0], match.dangerous_attacks[1], match.match_result,
                               match_lineups_json[0], match_lineups_json[1]))

        self.save_teams([match.home_team, match.away_team])
        self._SQL_Connection.commit()

    def save_matches(self, match_list: List[Match]):
        for match in match_list:
            self.save_match(match)

    def save_team(self, team: Team):
        DATABASE_LOGGER.info(f"Saving team {team.team_name} into database.")
        cursor = self._SQL_Connection.cursor()
        try:
            cursor.execute("INSERT INTO teams (team_id, team_name) VALUES (?, ?)", ("NULL", team.team_name))
        except mariadb.IntegrityError as e:
            print(f"Skipping duplicate team {team.team_name}")
            DATABASE_LOGGER.info(f"Team {team.team_name} already exists in database, no changes made.")

    def save_teams(self, team_list: List[Team]):
        for team in team_list:
            self.save_team(team)

    def load_match_by_id(self, match_id: int) -> Match:
        cursor = self._SQL_Connection.cursor()
        cursor.execute(f"SELECT * FROM matches WHERE match_id={str(match_id)}")
        return self.parse_matches_from_sql_cursor(cursor)[0]

    def load_matches_by_id(self, match_ids: List[int]) -> List[Match]:
        match_list = []
        for match_id in match_ids:
            match_list.append(self.load_match_by_id(match_id))
        return match_list

    def load_matches_by_club_name(self, club_name: str):
        cursor = self._SQL_Connection.cursor()
        cursor.execute(
            f"SELECT * FROM matches WHERE away_team_id={SQL_Connection.team_id_map[club_name]} OR "
            f"home_team_id={SQL_Connection.team_id_map[club_name]}")
        return self.parse_matches_from_sql_cursor(cursor)
