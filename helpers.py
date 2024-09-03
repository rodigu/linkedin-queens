from typing import Literal


Coords = tuple[int, int]
Board = list[list[str]]

class Queens:
    def __init__(self, board: Board):
        self._board: Board = board
        self.group_has_queen: dict[str, bool] = {}
        self.row_has_queen: list[bool] = [False for _ in range(len(self._board[0]))]
        self.col_has_queen: list[bool] = [False for _ in range(len(self._board))]
        self.queens_added: int = 0
        self.add_nodes()
    def add_nodes(self):
        for _, row in enumerate(self._board):
            for _, group in enumerate(row):
                if group not in self.group_has_queen: self.group_has_queen[group] = False
    def get_board(self) -> str:
        return ('\n').join([('').join(f'{r}') for r in self._board])
    def group_for(self, pos: Coords) -> str:
        return self._board[pos[1]][pos[0]][0]
    def queen_at(self, pos: Coords):
        return 'q' in self._board[pos[1]][pos[0]]
    def queen_in_neighborhood(self, pos: Coords) -> bool:
        x, y = pos
        if y - 1 > 0 and x - 1 > 0 and not self.queen_at((x-1, y-1)): return True
        if y - 1 > 0 and self.queen_at((x, y-1)): return True
        if y - 1 > 0 and x + 1 < len(self._board[y]) - 1 and self.queen_at((x+1, y-1)): return True
        if x - 1 > 0 and self.queen_at((x-1, y)): return True
        if x + 1 < len(self._board) - 1 and self.queen_at((x+1, y)): return True
        if y + 1 < len(self._board) - 1 and x - 1 > 0 and self.queen_at((x-1, y)): return True
        if y + 1 < len(self._board) - 1 and self.queen_at((x, y+1)): return True
        if y + 1 < len(self._board) - 1 and x + 1 < len(self._board[y]) - 1 and self.queen_at((x+1, y+1)): return True
        return False
    def add_queen(self, pos: Coords) -> bool:
        g = self.group_for(pos)
        if self.queen_at(pos) or self.queen_in_neighborhood(pos) or self.row_has_queen[pos[1]] or self.col_has_queen[pos[0]] or self.group_has_queen[g]:
            return False
        self.queens_added += 1
        self.row_has_queen[pos[1]] = True
        self.col_has_queen[pos[0]] = True
        self.group_has_queen[g] = True
        self._board[pos[1]][pos[0]] += 'q'
        return True
    def remove_queen(self, pos: Coords):
        self._board[pos[1]][pos[0]] = self._board[pos[1]][pos[0]][0]
        self.queens_added -= 1
        self.row_has_queen[pos[1]] = False
        self.col_has_queen[pos[0]] = False
        self.group_has_queen[self.group_for(pos)] = False
    def can_add_queen(self):
        for q in self.group_has_queen.values():
            if not q: return True
        return False
    def solved(self):
        return self.queens_added == len(self.group_has_queen)

def brute(board: Board, iter_limit: int = 1000) -> str:
    q = Queens(board)
    pos_history = []
    def next_pos(pos: Coords) -> Coords | Literal[False]:
        x, y = pos
        if x + 1 < len(board[y]) - 1: return (x + 1, y)
        elif y + 1 < len(board) - 1: return (0, y + 1)
        return False
    p: Coords = (0, 0)
    iterations = 0
    while not q.solved() or iterations >= iter_limit:
        print(iterations)
        print(pos_history)
        iterations += 1
        if q.add_queen(p):
            pos_history.append(p)
            if next_pos(p): p = next_pos(p)
            else: break
        print(q.get_board())
        if next_pos(p): p = next_pos(p)
        else:
            np = pos_history.pop()
            q.remove_queen(np)
            p = next_pos(np)
    return q.get_board()

if __name__=='__main__':
    b: Board = [list(r) for r in 'aabbbbbc-adddbbbc-aaadeeec-adddefec-gggdeeec-gdddhhec-ggggeeec-gggggccc'.split('-')]
    print(brute(b))