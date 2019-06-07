import pytest
import api


@pytest.fixture
def client():
    api.app.config['TESTING'] = True
    client = api.app.test_client()
    yield client


def test_game(client):
    ## new game
    res = client.post('/drop_token', json={
            'players': ['player1', 'player2'],
            'rows': 9,
            'columns': 9
        })
    game_id = res.json['gameId']

    # did it work?
    res = client.get('/drop_token')
    print(res.json)
    games = res.json['games']
    assert game_id in games

    # make a move
    res = client.post(f'/drop_token/{game_id}/player1', json={
        'column': 0
        })

    # inspect the move
    url = '/drop_token/' + res.json['move']
    res = client.get(url)
    print(res.json)

    assert res.json['type'] == 'MOVE'
    assert res.json['player'] == 'player1'
    assert res.json['column'] == 0

    # examine the state of the game
    res = client.get(f'/drop_token/{game_id}')
    print(res.json)
    players = res.json['players']
    assert len(players) == 2
    assert res.json['state'] == 'IN_PROGRESS'
    assert 'winner' not in res.json

    # make more moves
    for i in range(3):
        res = client.post(f'/drop_token/{game_id}/player2', json={
            'column': 1
            })
        res = client.post(f'/drop_token/{game_id}/player1', json={
            'column': 0
            })

    # game should be over now
    res = client.get(f'/drop_token/{game_id}')
    print(res.json)
    players = res.json['players']
    assert len(players) == 2
    assert res.json['state'] == 'DONE'
    assert res.json['winner'] == 'player1'

    # Try to make a move after game is over
    res = client.post(f'/drop_token/{game_id}/player2', json={
        'column': 1
        })
    assert res.status_code == 410

    ## test list-moves api
    res = client.get(f'/drop_token/{game_id}/moves')
    print(res.json)
    assert 'moves' in res.json

    for i, move in enumerate(res.json['moves']):
        assert move['player'] == 'player' + str(i%2+1)
        assert move['column'] == i%2
        assert move['type'] == 'MOVE'


def test_draw(client):
    ## new game
    res = client.post('/drop_token', json={
            'players': ['jane', 'henry'],
            'rows': 4,
            'columns': 2
        })
    game_id = res.json['gameId']

    # make more moves
    for i in range(4):
        res = client.post(f'/drop_token/{game_id}/jane', json={
            'column': i%2
            })
        res = client.post(f'/drop_token/{game_id}/henry', json={
            'column': i%2
            })

    # it's a draw
    res = client.get(f'/drop_token/{game_id}')
    print(res.json)
    players = res.json['players']
    assert len(players) == 2
    assert res.json['state'] == 'DONE'
    assert res.json['winner'] is None


def test_quit(client):
    ## new game
    res = client.post('/drop_token', json={
            'players': ['foo', 'bar', 'bat'],
            'rows': 7,
            'columns': 7
        })
    game_id = res.json['gameId']

    res = client.post(f'/drop_token/{game_id}/foo', json={
        'column': 0
        })
    res = client.post(f'/drop_token/{game_id}/bar', json={
        'column': 1
        })
    res = client.delete(f'/drop_token/{game_id}/bat')

    ## test list-moves api
    res = client.get(f'/drop_token/{game_id}/moves')
    print(res.json)
    assert 'moves' in res.json
    assert res.json['moves'][0] == {'column': 0, 'player': 'foo', 'type': 'MOVE'}
    assert res.json['moves'][1] == {'column': 1, 'player': 'bar', 'type': 'MOVE'}
    assert res.json['moves'][2] == {'player': 'bat', 'type': 'QUIT'}

    for i in range(2):
        res = client.post(f'/drop_token/{game_id}/foo', json={
            'column': 0
            })
        res = client.post(f'/drop_token/{game_id}/bar', json={
            'column': 1
            })

    ## list moves
    res = client.get(f'/drop_token/{game_id}/moves')
    print(res.json)
    assert len(res.json['moves']) == 7

    ## partial list moves
    res = client.get(f'/drop_token/{game_id}/moves?start=0&until=4')
    print(res.json)
    assert len(res.json['moves']) == 4

    ## get individual moves
    res = client.get(f'/drop_token/{game_id}/moves/1')
    assert res.json['type'] == 'MOVE'

    res = client.get(f'/drop_token/{game_id}/moves/2')
    assert res.json['type'] == 'QUIT'

    res = client.get(f'/drop_token/{game_id}')
    print(res.json)
    players = res.json['players']
    assert len(players) == 3
    assert res.json['state'] == 'IN_PROGRESS'

    res = client.delete(f'/drop_token/{game_id}/bar')

    # game should be over now
    res = client.get(f'/drop_token/{game_id}')
    print(res.json)
    players = res.json['players']
    assert len(players) == 3
    assert res.json['state'] == 'DONE'
    assert res.json['winner'] == 'foo'


def test_multiple_games(client):
    games = [
        {'players': ['ann', 'ben', 'carl'], 'rows': 7, 'cols': 7},
        {'players': ['dan', 'emma'],        'rows': 4, 'cols': 5},
        {'players': ['fred', 'gwen'],       'rows': 9, 'cols': 7},
    ]
    game_ids = []
    for a in games:
        res = client.post('/drop_token', json={
                'players': a['players'],
                'rows': a['rows'],
                'columns': a['cols']
            })
        game_ids.append(res.json['gameId'])

    res = client.get('/drop_token')
    print(res.json)
    assert all(game_id in res.json['games'] for game_id in game_ids)

    def play_game(game_id, players):
        for i in range(4):
            for player_id in players:
                res = client.post(f'/drop_token/{game_id}/{player_id}', json={
                    'column': i
                    })

                res = client.get(f'/drop_token/{game_id}')
                if res.json['state'] == 'DONE':
                    return

    play_game(game_ids[0], games[0]['players'])

    res = client.get(f'/drop_token/{game_ids[1]}')
    assert res.json['state'] == 'IN_PROGRESS'

    res = client.get(f'/drop_token/{game_ids[2]}')
    assert res.json['state'] == 'IN_PROGRESS'

    play_game(game_ids[1], games[1]['players'])

    res = client.get(f'/drop_token/{game_ids[0]}')
    assert res.json['state'] == 'DONE'

    res = client.get(f'/drop_token/{game_ids[1]}')
    assert res.json['state'] == 'DONE'

    res = client.get(f'/drop_token/{game_ids[2]}')
    assert res.json['state'] == 'IN_PROGRESS'

