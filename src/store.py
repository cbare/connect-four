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
ASSIGNED_TOKENS = set()
POSSIBLE_TOKENS = 'abcdefghijklmnopqrstuvwxyz!@#$%^&*-+='


def _assign_unique_token(proposed_token=None):
    """
    A hokey way of giving out unique tokens.
    """
    ## use the proposed token if not already assigned
    if proposed_token and proposed_token not in ASSIGNED_TOKENS:
        ASSIGNED_TOKENS.add(proposed_token)
        return proposed_token

    ## assign a symbol from back of list
    for t in reversed(POSSIBLE_TOKENS):
        if t not in ASSIGNED_TOKENS:
            ASSIGNED_TOKENS.add(t)
            return t

    ## fresh out of tokens
    raise RuntimeError('All tokens used.')


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
        p = Player(player_id, token=_assign_unique_token(player_id[0] if player_id else None))
        PLAYERS[player_id] = p
    return PLAYERS[player_id]


def get_player(player_id):
    if player_id not in PLAYERS:
        raise KeyError(f'Player "{player_id}" does not exist.')
    return PLAYERS[player_id]

