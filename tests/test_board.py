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
