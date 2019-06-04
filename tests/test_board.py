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
    b = game.Board(3,4)

    b.play(1, 'r')
    b.play(1, 'r')
    b.play(2, 'b')

    with pytest.raises(ValueError):
        b[0,0,0,0]

    with pytest.raises(IndexError):
        b[0,999]

    with pytest.raises(IndexError):
        b.play(999, 'z')
