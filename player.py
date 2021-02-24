import hashlib
from typing import List
from team import Team


class Player:
    all_players = {}

    def __init__(self, player_team_name, player_name):
        self.player_team_name = player_team_name
        self.player_name = player_name
        self.player_id = 0
        self.player_team_id = 0
        self.attributes = {'player_attack': 0, 'player_skill': 0, 'player_movement': 0, 'player_power': 0, 'player_mentality': 0, 'player_defending': 0}
        Player.all_players[self.md5(player_team_name, player_name)] = self

    @staticmethod
    def get_or_create_player(player_team_name, player_name):
        if Player.all_players.get(Player.md5(player_team_name, player_name)) is None:
            return Player(player_team_name, player_name)
        return Player.all_players.get(Player.md5(player_team_name, player_name))

    @staticmethod
    def player_from_csv_row(csv_row: List[str]):
        p = Player.get_or_create_player(player_name=csv_row[1], player_team_name=csv_row[3])
        p.player_id = csv_row[0] if csv_row[0] != 0 else p.player_id
        p.player_id = csv_row[2] if csv_row[2] != 0 else p.player_id
        p.attributes['player_attack'] = int(csv_row[4])
        p.attributes['player_movement'] = int(csv_row[5])
        p.attributes['player_mentality'] = int(csv_row[6])
        p.attributes['player_defending'] = int(csv_row[7])
        p.attributes['player_power'] = int(csv_row[8])
        p.attributes['player_skill'] = int(csv_row[9])
        return p

    def get_team(self):
        return Team.all_teams.get(self.player_team_name)

    def __str__(self):
        return 'Player: %-26s\t\tTeam: %-16s\tATK: %2d\tMOV: %2d\tMEN: %2d\tDEF: %2d\tPOW: %2d\tSKI: %2d' % \
               (self.player_name,
                self.player_team_name,
                self.attributes['player_attack'],
                self.attributes['player_movement'],
                self.attributes['player_mentality'],
                self.attributes['player_defending'],
                self.attributes['player_power'],
                self.attributes['player_skill']
                )

    def as_csv_row(self) -> str:
        return str('%d,%s,%d,%s,%d,%d,%d,%d,%d,%d' % \
               (
                int(self.player_id),
                self.player_name,
                int(self.player_team_id),
                self.player_team_name,
                int(self.attributes['player_attack']),
                int(self.attributes['player_movement']),
                int(self.attributes['player_mentality']),
                int(self.attributes['player_defending']),
                int(self.attributes['player_power']),
                int(self.attributes['player_skill'])
                ))

    @staticmethod
    def md5(player_team_name, player_name):
        return hashlib.md5((player_team_name + player_name).encode('utf-8'))
