import json, sys, mariadb, csv
import numpy as np, pandas as pd
from sql_connection import SQL_Connection

sql = SQL_Connection.get_or_init_sql_connection()

def calculate_teams(id):
    lineups = sql.load_match_by_id(id)
    home_name, home_team = lineups[0], lineups[2]
    away_name, away_team = lineups[1], lineups[3]
    match_result = lineups[4]
    home_array, away_array = np.array([0, 0, 0, 0, 0, 0], dtype=np.int32), np.array([0, 0, 0, 0, 0, 0], dtype=np.int32)
    home_non_exist, away_non_exist = 0, 0

    for i in range(len(home_team)):
        player_name = home_team[i].split()
        cursor.execute(f"SELECT * FROM players WHERE player_team LIKE '%{str(home_name)}%' "
                       f"AND player_name LIKE '%{str(player_name[0])}%'")
        result = cursor.fetchall()
        if len(result) > 0:
            newarray = np.array(result[0][3:], dtype=np.int32)
            home_array = np.add(home_array, newarray)
        else:
            home_non_exist += 1

    for i in range(len(away_team)):
        player_name = away_team[i].split()
        cursor.execute(f"SELECT * FROM players WHERE player_team LIKE '%{str(away_name)}%' "
                       f"AND player_name LIKE '%{str(player_name[0])}%'")
        result = cursor.fetchall()
        if len(result) > 0:
            newarray = np.array(result[0][3:], dtype=np.int32)
            away_array = np.add(away_array, newarray)
        else:
            away_non_exist += 1

    home_attrs, away_attrs = np.array(home_array / (len(home_team) - home_non_exist)), \
                             np.array(away_array / (len(away_team) - away_non_exist))
    match_attrs = np.subtract(home_attrs, away_attrs)
    match_attrs = np.append(match_attrs.round(3), match_result)
    return match_attrs


with open("PL_data.csv", mode='a') as csv_file:
    writer = csv.writer(csv_file)
    for a in range(16, 26):
        match = calculate_teams(a)
        writer.writerow(match)
