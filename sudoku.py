import numpy as np
from math import floor
from copy import deepcopy


class Sudoku:
    def __init__(self):
        self.board = []

    def read_from_file(self, path="examples/1.sdk"):
        self.path = path
        b = []
        with open(path) as f:
            a = f.readlines()
            for line in a:
                t = []
                for char in line:
                    if char in [str(i) for i in range(1, 10)] + ['_']:
                        t.append(list([i for i in range(1, 10)]) if char == '_' else int(char))
                b.append(t)
        self.board = np.array(b)

    def write_to_file(self, path=None):
        p = self.path.split(".")[0] if hasattr(self, 'path') else 'sol'
        with open(path if path is not None else p + ".sol", 'w') as f:
            for l in self.board:
                for c in l:
                    f.write(str(c) if type(c) != list else '_')
                f.write('\n')

    def set_board(self, board):
        self.board=[]
        for l in range(9):
            self.board.append([])
            for c in range(9):
                self.board[l].append(board[l][c] if (board[l][c] not in [0, None]) else [i for i in range(1,10)])
        self.board = np.array(self.board)

    def __str__(self):
        ret=""
        for item in self.board:
            for cell in item:
                ret+=(str(cell) if type(cell) in [int, np.int64] else '_')+" "
            ret+="\n"
        return ret[:-1]

    def __repr__(self):
        return str(self)

    def print_board_with_options(self):
        b_state = self.get_progress()
        print("Board is {}% complete({}/81)".format(b_state[0], b_state[1]))
        for item in self.board:
            for cell in item:
                if type(cell) in [int, np.int64]:
                    print("    " + str(cell) + "     ", end="")
                else:
                    size = 10 - len(cell)
                    print(" " * (size // 2), end="")
                    print("".join([str(i) for i in cell]), end="")
                    print(" " * ((size // 2) + size % 2), end="")
            print("")

    def get_progress(self):
        cells_filled = 0
        for l in range(9):
            for c in range(9):
                if type(self.board[l][c]) in [int, np.int64]:
                    cells_filled += 1
        return floor(100 * (cells_filled / 81)), cells_filled

    def validate_board(self):
        result = np.array(list(range(1, 10)))
        for l in self.board:
            if any(type(cell) == list for cell in l):
                return False
            if not np.array_equal(np.sort(l), result):
                return False
        for c in range(9):
            if not np.array_equal(np.sort(self.board[:, c]), result):
                return False
        for l in range(3):
            for c in range(3):
                if not np.array_equal(np.sort(np.reshape(self.board[l * 3:l * 3 + 3, c * 3:c * 3 + 3], -1)), result):
                    return False
        return True

    def validate_cell_new_val(self, l, c, val):
        res = True
        if self.board[l][c] == val:
            self.board[l][c] = 0

        if val in self.board[l]:
            res = False
        if val in self.board[:, c]:
            res = False
        if val in np.reshape(self.board[3 * (l // 3):3 * (l // 3) + 3, 3 * (c // 3):3 * (c // 3) + 3], -1):
            res = False

        if self.board[l][c] == 0:
            self.board[l][c] = val

        return res

    def _remove_cell_option(self, l, c, val):
        if type(self.board[l][c]) is list:
            if val in self.board[l][c]:
                self.board[l][c].remove(val)
            if len(self.board[l][c]) == 1:
                # self.board[l][c] = int(self.board[l][c][0])
                self.write_in_cell(l, c, int(self.board[l][c][0]))

    def _remove_from_line(self, l, val):
        for c in range(9):
            self._remove_cell_option(l, c, val)

    def _remove_from_column(self, c, val):
        for l in range(9):
            self._remove_cell_option(l, c, val)

    def _remove_from_square(self, l, c, val):
        for l1 in range(3):
            for c1 in range(3):
                self._remove_cell_option(3 * (l // 3) + l1, 3 * (c // 3) + c1, val)

    def write_in_cell(self, l, c, val: int):
        self.board[l][c] = val
        self._remove_from_line(l, val)
        self._remove_from_column(c, val)
        self._remove_from_square(l, c, val)

    def remove_options_known(self):
        for l in range(9):
            for c in range(9):
                if type(self.board[l][c]) in [int, np.int64]:
                    self._remove_from_line(l, self.board[l][c])
                    self._remove_from_column(c, self.board[l][c])
                    self._remove_from_square(l, c, self.board[l][c])

    @staticmethod
    def _find_unique_in_group(group):
        """
        :param group: mus be a 1d list/array with 9 elements
        :return:
            list of uniques
        """
        unique = []
        pos = []
        for val in range(1, 10):
            t = 0
            last_p = 0
            if val not in group:
                for i in range(9):
                    if type(group[i]) is list:
                        if val in group[i]:
                            t = t + 1
                            last_p = i
                if t == 1:
                    unique.append(val)
                    pos.append(last_p)
        return unique, pos

    def find_unique_in_lines(self):
        for l in range(9):
            u, p = self._find_unique_in_group(self.board[l])
            for val, pos in zip(u, p):
                self.write_in_cell(l, pos, val)

    def find_unique_in_columns(self):
        for c in range(9):
            u, p = self._find_unique_in_group(self.board[:, c])
            for val, pos in zip(u, p):
                self.write_in_cell(pos, c, val)

    def find_unique_in_square(self):
        for l in range(3):
            for c in range(3):
                u, p = self._find_unique_in_group(np.reshape(self.board[l * 3:l * 3 + 3, c * 3:c * 3 + 3], -1))
                for val, pos in zip(u, p):
                    l1 = pos // 3
                    c1 = pos % 3
                    self.write_in_cell(l * 3 + l1, c * 3 + c1, val)

    @staticmethod
    def find_pack_in_group(group):
        pos = list([list([]) for i in range(9)])
        for val in range(1, 10):
            for i in range(9):
                if type(group[i]) is list:
                    if val in group[i]:
                        pos[val - 1].append(i)
        return pos

    @staticmethod
    def find_duplicates(elements):
        ''' returns list of duplicates '''
        unique_elements = list(np.unique(np.array(elements)))
        # print(elements)
        duplicates = []

        for elem in unique_elements:
            if elements.count(elem) > 1:
                duplicates.append(elem)
        if [] in duplicates:
            duplicates.remove([])
        return duplicates

    def find_pack_in_squares(self):
        for l in range(3):
            for c in range(3):
                pos = self.find_pack_in_group(np.reshape(self.board[l * 3:l * 3 + 3, c * 3:c * 3 + 3], -1))
                for dup in self.find_duplicates(pos):
                    opt = []
                    if len(dup) == 2:
                        opt.append(pos.index(dup) + 1)
                        opt.append(pos.index(dup, opt[0]) + 1)
                        for p in range(9):
                            if p in dup:
                                self.board[l * 3 + (p // 3)][c * 3 + (p % 3)] = list(opt)
                            else:
                                self._remove_cell_option(l * 3 + (p // 3), c * 3 + (p % 3), opt[0])
                                self._remove_cell_option(l * 3 + (p // 3), c * 3 + (p % 3), opt[1])

    def find_pack_in_lines(self):
        for l in range(9):
            pos = self.find_pack_in_group(self.board[l])
            for dup in self.find_duplicates(pos):
                opt = []
                if len(dup) == 2:
                    opt.append(pos.index(dup) + 1)
                    opt.append(pos.index(dup, opt[0]) + 1)
                    for c in range(9):
                        if c in dup:
                            self.board[l][c] = list(opt)
                        else:
                            self._remove_cell_option(l, c, opt[0])
                            self._remove_cell_option(l, c, opt[1])
                    # for p in dup:
                    # self.write_in_cell(l,p,opt)
                    # self.board[l][p] = list(opt)

    def find_pack_in_column(self):
        for c in range(9):
            pos = self.find_pack_in_group(self.board[:, c])
            for dup in self.find_duplicates(pos):
                opt = []
                if len(dup) == 2:
                    opt.append(pos.index(dup) + 1)
                    opt.append(pos.index(dup, opt[0]) + 1)
                    for l in range(9):
                        if l in dup:
                            self.board[l][c] = list(opt)
                        else:
                            self._remove_cell_option(l, c, opt[0])
                            self._remove_cell_option(l, c, opt[1])
                    # for p in dup:
                    # self.write_in_cell(p, c, opt)
                    # self.board[p][c] = list(opt)

    def list_missing_cells(self):
        options = [[0 for i in range(9)] for i in range(9)]
        for l in range(9):
            for c in range(9):
                if type(self.board[l][c]) not in [int, np.int64]:
                    options[l][c] = len(self.board[l][c])

        coord = []
        for i in range(2, 10):
            for l in range(9):
                for c in range(9):
                    if options[l][c] == i:
                        coord.append([l, c])
        return coord

    def _brute_force(self, coord, i=0):
        if len(coord) == i:
            return self.validate_board()

        next_coord = coord[i]

        if type(self.board[next_coord[0]][next_coord[1]]) != list:
            if self.validate_cell_new_val(next_coord[0], next_coord[1], self.board[next_coord[0]][next_coord[1]]):
                return self._brute_force(coord, i + 1)
            else:
                self.board[next_coord[0]][next_coord[1]] = list(self.possibilities_board[next_coord[0]][next_coord[1]])
                return False

        else:
            possibilities = list(self.board[next_coord[0]][next_coord[1]])

        while True:
            next_val = possibilities.pop()

            if self.validate_cell_new_val(next_coord[0], next_coord[1], next_val):
                state = deepcopy(self.board)
                self.write_in_cell(next_coord[0], next_coord[1], next_val)
                # print("{},{}->{}".format(next_coord[0],next_coord[1],next_val))
                if self._brute_force(coord, i + 1):
                    return True
                else:
                    self.board = deepcopy(state)

            if len(possibilities) == 0:
                self.board[next_coord[0]][next_coord[1]] = list(self.possibilities_board[next_coord[0]][next_coord[1]])
                return False

    def start_brute_force(self):
        coord = self.list_missing_cells()
        self.possibilities_board = deepcopy(self.board)
        return self._brute_force(coord, 0)

    def solve(self):
        l_board = deepcopy(self.board)
        while True:
            self.remove_options_known()
            self.find_unique_in_columns()
            self.find_unique_in_lines()
            self.find_unique_in_square()
            self.find_pack_in_squares()
            self.find_pack_in_lines()
            self.find_pack_in_column()
            if np.array_equal(self.board, l_board):
                break
            else:
                l_board = deepcopy(self.board)
            return self.start_brute_force()


if __name__ == '__main__':
    import time

    start = time.time()
    sudoku = Sudoku()
    # sudoku.read_from_file('examples/6.sdk')
    sudoku.set_board([
        [0, 8, 0, 0, 2, 0, 5, 6, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 7],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 0, 0, 9, 0, 4, 0, 8],
        [0, 0, 7, 8, 0, 0, 0, 0, 3],
        [0, 9, 0, 0, 1, 0, 0, 5, 0],
        [2, 0, 4, 0, 0, 0, 8, 0, 0],
        [0, 6, 0, 0, 8, 5, 0, 0, 0],
        [0, 0, 0, 2, 0, 0, 1, 0, 0]
    ])
    if sudoku.solve():
        print("Solved")
        sudoku.write_to_file()
    else:
        print("Impossible to solve")
    print(sudoku)
    print(time.time() - start)
