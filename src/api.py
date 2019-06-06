"""
"""
import store
from game import ColumnFullException, OutOfTurnError, GameOver

from flask import Flask
from flask import jsonify, request
import jsonschema
from jsonschema import validate


app = Flask('connect_four')


#----------------------------------------------------------------------
#  JSON schemas
#----------------------------------------------------------------------

GAME_SCHEMA = {
    'type': 'object',
    'players': {
        'type': 'array',
        'items': {'type': 'number'},
        'minitems': 1,
        'maxitems': 26,
    },
    'rows': {'type': 'integer'},
    'columns': {'type': 'integer'},
    'required': ['players', 'rows', 'columns'],
}

MOVE_SCHEMA = {
    'type': 'object',
    'column': {'type': 'integer'},
    'required': ['column'],
}


#----------------------------------------------------------------------
#  Helpers
#----------------------------------------------------------------------

def _get_game(game_id):
    """
    Get a game based on a user-provided ID. If it's not a valid ID, respond
    with a 404 error.
    """
    try:
        return store.get_game(game_id)
    except KeyError as error:
        raise ClientError(error, status_code=404)


def _get_player(player_id):
    """
    Get a player based on a user-provided ID. If it's not a valid ID, respond
    with a 404 error.
    """
    try:
        return store.get_player(player_id)
    except KeyError as error:
        raise ClientError(error, status_code=404)


def _history_to_dict(history):
    """
    Turn list of moves into a dictionary
    """
    return {
        'moves': [
            {'type': 'QUIT', 'player': player.id} if col < 0 else \
            {'type': 'MOVE', 'player': player.id, 'column': col} \
                for player, col in history]
    }



#----------------------------------------------------------------------
#  Routes
#----------------------------------------------------------------------

@app.route('/')
def home():
    return jsonify({'message': 'Hello, World!'})


## Return all in-progress games or create a new game.
@app.route('/drop_token')
def list_games():
    return jsonify({'games': store.list_games()})


## Create a new game.
@app.route('/drop_token', methods=['POST'])
def new_game():
    data = request.get_json()
    validate(data, GAME_SCHEMA)

    player_ids = data['players']
    rows, columns = data['rows'], data['columns']

    game = store.new_game(player_ids, rows, columns)
    return jsonify({
            'gameId': game.id
        })


## GET the state of the game.
@app.route('/drop_token/<game_id>')
def get_game(game_id):
    game = _get_game(game_id)
    output = {
        "players" : [player.id for player in game.players],
        "state": game.status,
    }
    if game.status=='DONE':
        output['winner'] = game.winner.id if game.winner else None
    return jsonify(output)


@app.route('/drop_token/<game_id>/moves')
def list_moves(game_id):
    """
    GET the list of moves played in a game or a sub-range that list.
    """
    game = _get_game(game_id)

    start = request.args.get('start', 0)
    until = request.args.get('until', None)
    return jsonify(_history_to_dict(game.history[start:until]))


## GET a move.
@app.route('/drop_token/<game_id>/moves/<int:move_number>')
def get_move(game_id, move_number):
    game = _get_game(game_id)

    if move_number < 0 or move_number > len(game.history):
        raise ValueError(f'Move number {move_number} does not exist.')

    player, column = game.history[move_number]

    return jsonify({
            'type': 'MOVE',
            'player': player.id,
            'column': column
        })


@app.route('/drop_token/<game_id>/<player_id>', methods=['POST'])
def play_move(game_id, player_id):
    """
    POST a move
    """
    game = _get_game(game_id)
    player = _get_player(player_id)

    data = request.get_json()
    validate(data, MOVE_SCHEMA)
    column = data['column']

    try:
        move_number = game.play(player, column)
    except IndexError as error:
        raise ClientError(error, status_code=400)

    return jsonify({
            'move': f'{game_id}/moves/{move_number}',
        })


@app.route('/drop_token/<game_id>/<player_id>', methods=['DELETE'])
def quit(game_id, player_id):
    """
    Player quits.
    """
    game = _get_game(game_id)
    player = _get_player(player_id)

    game.quit(player)

    # return empty body, status code 202
    return '', 202


#----------------------------------------------------------------------
#  Error handling
#----------------------------------------------------------------------

class ClientError(Exception):
    """
    Wrap another exception to signal that this is a client error.
    """
    def __init__(self, error, status_code=400):
        self.args = error.args
        self.status_code = status_code


@app.errorhandler(ClientError)
@app.errorhandler(jsonschema.exceptions.ValidationError)
@app.errorhandler(GameOver)
@app.errorhandler(OutOfTurnError)
@app.errorhandler(ColumnFullException)
def handle_client_error(error):
    """
    Turn a Python exception into an appropriate HTTP response.
    """
    fields = {'exception': str(type(error))}

    if hasattr(error, 'args') and len(error.args) > 0:
        fields['message'] = error.args[0]
    response = jsonify(fields)

    if hasattr(error, 'status_code') and error.status_code is not None:
        response.status_code = error.status_code
    else:
        response.status_code = 400

    return response

