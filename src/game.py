"""
"""
import io


class ColumnFullException(Exception):
    pass


class Board():
    """
    Represent a game board with _n_ rows and _m_ columns.
    """
    def __init__(self, n=4, m=4):
        self.n = n
        self.m = m
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
        if len(t)==0:
            return self.board
        if len(t)==1:
            return [self.board[j][t[0]] for j in range(self.m)]
        if len(t)==2:
            return self.board[t[1]][t[0]]
        raise ValueError(f'{len(t)} is the wrong number of dimensions.')

    def play(self, column, piece):
        """
        Play a piece in the specified column.
        """
        if column < 0 or column >= self.m:
            raise ValueError(f'Column {column} doesn\'t exist.')

        for i in range(self.n):
            if self.board[column][i] == ' ':
                self.board[column][i] = piece
                break
        else:
            raise ColumnFullException(f'Can\'t play in column {column}. That column is full.')
