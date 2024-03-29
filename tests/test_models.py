import pytest

import game


def test_board():
    b = game.Board(3,4)

    assert b[0,0] == ' '
    assert b[2,3] == ' '

    b.play(1, 'r')
    b.play(1, 'r')
    b.play(2, 'b')

    print(b)

    assert b[0,1] == 'r'
    assert b[1,1] == 'r'
    assert b[2,1] == ' '
    assert b[0,2] == 'b'
    assert b[1,2] == ' '

    ## get row of b
    assert len(b[1]) == 4

    ## get column of b
    assert b[:,1] == ['r', 'r', ' ']


def test_board_error_handling():
    b = game.Board(2,4)

    b.play(1, 'r')
    b.play(1, 'r')
    b.play(2, 'b')

    with pytest.raises(ValueError):
        b[0,0,0,0]

    with pytest.raises(IndexError):
        b[0,999]

    with pytest.raises(IndexError):
        b.play(999, 'z')

    with pytest.raises(game.ColumnFullException):
        b.play(1, 'z')


def test_board_is_full():
    b = game.Board(3,2)

    assert not b.is_full()

    for i in range(2):
        b.play(1, 'r')
        assert not b.is_full()
        b.play(0, 'b')
        assert not b.is_full()

    b.play(1, 'r')
    assert not b.is_full()
    b.play(0, 'b')
    assert b.is_full()


def test_is_winning_move_vertical():
    b = game.Board(4,4)
    for i in range(3):
        b.play(0, 'x')
        b.play(1, 'o')
    assert b.is_winning_move(2,0,'x') is False
    assert b.is_winning_move(2,1,'y') is False
    assert b.is_winning_move(3,1,'y') is False

    b.play(0, 'x')
    assert b.is_winning_move(3,0,'x')


def test_is_winning_move_horizontal():
    b = game.Board(4,4)
    for i in range(3):
        b.play(i, 'x')
        b.play(i, 'o')
    assert b.is_winning_move(0,2,'x') is False
    assert b.is_winning_move(1,2,'y') is False

    b.play(3, 'x')
    assert b.is_winning_move(0,3,'x')


def test_is_winning_move_diagonal():
    b = game.Board(4,4)
    for i in range(4):
        for j in range(i):
            b.play(i, 'o')
        b.play(i, 'x')
    assert b.is_winning_move(3,3,'x')
    assert b.is_winning_move(0,0,'x')
    assert b.is_winning_move(1,1,'x')


def test_game():
    p = game.Player('Player1', '1')
    q = game.Player('Player2', '2')
    g = game.Game(p, q)

    with pytest.raises(game.OutOfTurnError):
        g.play(q, 0)

    move_number = g.play(p, 0)
    assert move_number == 0

    with pytest.raises(game.OutOfTurnError):
        g.play(p, 0)

    move_number = g.play(q, 0)
    assert move_number == 1


def test_quit_game():
    p = game.Player('Player1', '1')
    q = game.Player('Player2', '2')
    r = game.Player('Player3', '3')
    g = game.Game(p, q, r)

    assert g.status == 'IN_PROGRESS'

    g.quit(p)

    # can't play if you already quit
    with pytest.raises(ValueError):
        g.play(p, 0)

    # make sure other players can play
    g.play(q, 1)
    g.play(r, 1)

    # only 1 player left, so that player wins
    g.quit(q)
    assert g.status == 'DONE'
    assert g.winner == r


def test_win_game():
    p = game.Player('Player1', '1')
    q = game.Player('Player2', '2')
    g = game.Game(p, q)

    for i in range(3):
        g.play(p, 1)
        g.play(q, 2)

    assert g.status == 'IN_PROGRESS'

    g.play(p, 1)

    assert g.status == 'DONE'
    assert g.winner == p

