"""
This module is a stub implementation of an abstraction layer between the
game and some form of storage. This is a demo, so we store everything in
local memory.

Alternate implementations might include:
 - REDIS if your goal is distributed shared memory
 - PostgreSQL if your goal is to be transactional and persistent
 - Dynamo / Casandra if your goal is to be distributed and persistent
"""
from game import Game, Player

GAMES = {}
PLAYERS = {}


def get_game(game_id):
    if game_id not in GAMES:
        raise KeyError(f'Game {game_id} does not exist.')
    return GAMES[game_id]


def list_games():
    return list(GAMES.keys())


def new_game(player_ids, rows, columns):
    players = [get_or_create_player(player_id) for player_id in player_ids]
    g = Game(*players, n=rows, m=columns)
    GAMES[g.id] = g
    return g


def get_or_create_player(player_id):
    if player_id not in PLAYERS:
        p = Player(player_id)
        PLAYERS[player_id] = p
    return PLAYERS[player_id]


def get_player(player_id):
    if player_id not in PLAYERS:
        raise KeyError(f'Player "{player_id}" does not exist.')
    return PLAYERS[player_id]

