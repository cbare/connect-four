"""
"""
import store

from flask import Flask
from flask import jsonify, request

app = Flask('connect_four')



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
    player_ids = data['players']
    rows, columns = int(data['rows']), int(data['columns'])
    game = store.new_game(player_ids, rows, columns)
    return jsonify({
            'gameId': game.id
        })


## GET the state of the game.
@app.route('/drop_token/<game_id>')
def get_game(game_id):
    game = store.get_game(game_id)
    output = {
        "players" : [player.id for player in game.players],
        "state": game.status,
    }
    if game.status=='DONE':
        output['winner'] = game.winner.id if game.winner else None
    return jsonify(output)


## GET a range of moves.
@app.route('/drop_token/<game_id>/moves')
def list_moves(game_id):
    game = store.get_game(game_id)

    start = request.args.get('start', 0)
    until = request.args.get('until', len(game.history))
    return jsonify({
        "moves": [ {'type': 'MOVE', 'player': player_id, 'column': j}
                    for player_id, j in game.history[start:until] ]
        })


## GET a move.
@app.route('/drop_token/<game_id>/moves/<int:move_number>')
def get_move(game_id, move_number):
    game = store.get_game(game_id)

    if move_number < 0 or move_number > len(game.history):
        raise ValueError(f'Move number {move_number} does not exist.')

    player, column = game.history[move_number]

    return jsonify({
            'type': 'MOVE',
            'player': player.id,
            'column': column
        })


## POST a move.
@app.route('/drop_token/<game_id>/<player_id>', methods=['POST'])
def play_move(game_id, player_id):
    game = store.get_game(game_id)
    player = store.get_player(player_id)

    j = request.get_json()
    column = int(j['column'])

    move_number = game.play(player, column)

    return jsonify({
            'move': f'{game_id}/moves/{move_number}',
        })


## Player quits.
@app.route('/drop_token/<game_id>/<player_id>', methods=['DELETE'])
def quit(game_id, player_id):
    game = store.get_game(game_id)
    player = store.get_player(player_id)
    game.quit(player)

    return '', 202

