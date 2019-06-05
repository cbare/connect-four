"""
"""
import io
import uuid



class ColumnFullException(Exception):
    pass


class OutOfTurnError(ValueError):
    pass


class GameOver(Exception):
    pass



class Board():
    """
    Represent a game board with _n_ rows and _m_ columns. A win requires
    _k_ tokens of the same kind in a row, column or diagonal.
    """
    def __init__(self, n=4, m=4, k=4):
        if n < 1 or m < 1:
            raise ValueError(f'Can\'t create a board of dimensions ({n},{m}).')
        if k < 1:
            raise ValueError(f'Number of tokens in a row to win must be positive, not {k}.')
        self.n = n
        self.m = m
        self.k = k
        self.board = [[' ' for _ in range(n)] for _ in range(m)]

    def __repr__(self):
        return f'Board({self.n}, {self.m})'

    def __str__(self):
        out = io.StringIO()
        out.write('\n+' + '+'.join(f'---'  for j in range(self.m)) + '+\n')
        for i in range(self.n-1, -1, -1):
            out.write('|' + '|'.join(f' {self.board[j][i]} '  for j in range(self.m)) + '|\n')
            out.write('+' + '+'.join(f'---'  for j in range(self.m)) + '+\n')
        return out.getvalue()

    def __getitem__(self, t):
        """
        Get the contents of the game board based on a tuple (i,j) to get
        the contents of the i-th row (numbered from the bottom) and the j-th
        column, where i and j are zero based.
        """
        if type(t)==int:
            return [self.board[j][t] for j in range(self.m)]
        if len(t)==0:
            return self.board
        if len(t)==1:
            return [self.board[j][t[0]] for j in range(self.m)]
        if len(t)==2:
            return self.board[t[1]][t[0]]
        raise ValueError(f'{len(t)} is the wrong number of dimensions.')


    def play(self, column, token):
        """
        Play a token in the specified column.
        """
        if column < 0 or column >= self.m:
            raise IndexError(f'Column {column} doesn\'t exist.')

        for i in range(self.n):
            if self.board[column][i] == ' ':
                break
        else:
            raise ColumnFullException(f'Can\'t play in column {column}. That column is full.')

        self.board[column][i] = token

        return self.is_winning_move(i, column, token)


    def _find_win(self, i, j, token, di, dj):
        """
        Helper method for is_winning_move. Asks whether the slot i,j is a
        winning move. Is it part of k tokens in a row in the direction
        determined by di and dj.
        """
        count = 0

        d = 0
        while i+d*di<self.n and j+d*dj<self.m and i+d*di>=0 and j+d*dj>=0:
            if self[i+d*di, j+d*dj] == token:
                count += 1
            else:
                break
            d += 1

        di = di * -1
        dj = dj * -1
        d = 1
        while i+d*di<self.n and j+d*dj<self.m and i+d*di>=0 and j+d*dj>=0:
            if self[i+d*di, j+d*dj] == token:
                count += 1
            else:
                break
            d += 1

        return count >= self.k


    def is_winning_move(self, i, j, token):
        ## k in a row
        ## k in a column
        ## k in / diagonal
        ## k in \ diagonal
        return self._find_win(i, j, token, di=0, dj=1)  \
            or self._find_win(i, j, token, di=1, dj=0)  \
            or self._find_win(i, j, token, di=1, dj=1)  \
            or self._find_win(i, j, token, di=1, dj=-1)


    def is_full(self):
        for i in range(self.n):
            for j in range(self.m):
                if self[j,i] == ' ':
                    return False
        return True



class Player():
    def __init__(self, name, player_id=None, token=None):
        if (not name):
            raise ValueError('Give the player a non-empty name')
        self.name = name
        self.id = player_id if player_id else uuid.uuid4()
        self.token = token if token else name[0]

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f"Player('{self.name}', '{self.id}', '{self.token}')"



class Game():
    """
    A game of connect-four, with a board and a list of players.
    """
    def __init__(self, *args, n=4, m=4):
        self.id = uuid.uuid4()
        self.board = Board(n, m)
        self.players = args
        self.player_active = {player:True for player in args}
        self.turn = 0
        self.history = []
        self.winner = None

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f"Game('{self.id}')"


    @property
    def active_players(self):
        """
        returns the number of active players in the game.
        """
        return sum(active for player, active in self.player_active.items())


    @property
    def status(self):
        return 'DONE' if (self.winner or self.board.is_full() or self.active_players < 2) else 'IN_PROGRESS'


    def quit(self, player):
        """
        The specified player quits the game.
        """
        if player not in self.player_active:
            raise KeyError(f'{player.name} not in {self}.')
        self.player_active[player] = False

        ## if there's only one player left, that player wins
        if self.active_players == 1:
            for player, active in self.player_active.items():
                if active:
                    self.winner = player

        ## if the current player quits, figure out whose turn it is
        current_player = self.players[self.turn]
        if player == current_player:
            self._increment_turn()


    def play(self, player, column):
        """
        The given player places a token in the column specified.
        """
        if self.status == 'DONE':
            raise GameOver('Game Over')

        current_player = self.players[self.turn]
        if player != current_player:
            raise OutOfTurnError(f'{player.name} can\'t play right now. It\'s {current_player.name}\'s turn.')

        if not self.player_active.get(player, False):
            raise ValueError(f'{player.name} is not an active player in the game.')

        ## update board
        win = self.board.play(column, player.token)
        if win:
            self.winner = player

        ## record move in history
        self.history.append((player, column))

        self._increment_turn()


    def _increment_turn(self):
        """
        next active player's turn
        """
        i = 1
        while i < len(self.players) and not \
              self.player_active.get(self.players[(self.turn + i) % len(self.players)], False):
            i += 1
        self.turn = (self.turn + i) % len(self.players)

