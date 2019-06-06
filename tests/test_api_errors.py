import pytest
import api


@pytest.fixture
def client():
    api.app.config['TESTING'] = True
    client = api.app.test_client()
    yield client


def test_errorrz(client):
    players = ['player1', 'player2']

    res = client.post('/drop_token', json={
            'players': players,
            'rows': 4,
            'columns': 4
        })
    assert res.status_code == 200
    game_id = res.json['gameId']

    ## malformed request
    res = client.post('/drop_token', json={
            'players': ['harry', 'draco'],
            'quaffles': 1,
            'bludgers': 2,
            'snitch': 1
        })
    assert res.status_code == 400

    ## play out of turn
    res = client.post(f'/drop_token/{game_id}/player2', json={
        'column': 2
        })
    assert res.status_code == 409

    ## player not part of game
    res = client.post(f'/drop_token/{game_id}/monkey', json={
        'column': 2
        })
    assert res.status_code == 404

    ## bad game id
    res = client.post(f'/drop_token/zip-tang-ptow/player1', json={
        'column': 2
        })
    assert res.status_code == 404

    ## drop a token into a too-small column
    res = client.post(f'/drop_token/{game_id}/player1', json={
        'column': -1
        })
    assert res.status_code == 400

    ## drop a token into a too-large column
    res = client.post(f'/drop_token/{game_id}/player1', json={
        'column': 4
        })
    assert res.status_code == 400

    ## rando player tries to quit
    res = client.delete(f'/drop_token/{game_id}/randowackadoodle', json={
        'column': 4
        })
    assert res.status_code == 404

    ## fill up column 0
    for i in range(2):
        for player_id in players:
            res = client.post(f'/drop_token/{game_id}/{player_id}', json={
                'column': 0
                })
            assert res.status_code == 200

    ## get state of game
    res = client.get(f'/drop_token/{game_id}')
    assert res.json['state'] == 'IN_PROGRESS'

    ## get state on non-existant game
    res = client.get(f'/drop_token/fizzbuzz')
    assert res.status_code == 404

    ## drop a token into a full column
    res = client.post(f'/drop_token/{game_id}/player1', json={
        'column': 0
        })
    assert res.status_code == 400

    ## play in columns 2 and 3
    for i in range(3):
        for j, player_id in enumerate(players):
            res = client.post(f'/drop_token/{game_id}/{player_id}', json={
                'column': j + 2
                })
            assert res.status_code == 200

    ## winning move by player1
    res = client.post(f'/drop_token/{game_id}/player1', json={
        'column': 2
        })
    assert res.status_code == 200

    ## try to play after game is over
    res = client.post(f'/drop_token/{game_id}/player2', json={
        'column': 2
        })
    assert res.status_code == 410

    ## try to quit after game is over
    res = client.delete(f'/drop_token/{game_id}/player2')
    assert res.status_code == 410

    ## list moves with bad start / until query params

