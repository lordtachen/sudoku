import numpy as np
def read_sdk(path):
    l = []
    with open(path) as f:
        for line in f:
            t=[]
            for char in line:
                if char != '\n':
                    t.append(0 if char == '_' else int(char))
            l.append(t)
        return l



def printboard(board):
    for item in board:
        print(item)

def initia_possible_solutions(board):
    sol=np.array(board)
    for l in range(9):
        for c in range(9):
            if sol[l][c] == 0:
                sol[l][c]= np.array([i for i in range(1,10)])
    return sol

def validate_cell(board,l,c):
    if board[l][c] != 0:
        return board[l][c]
    else:
        p=possible_choices(board,l,c)
        if len(p)==1:
            return p[0]
        else:
            return 0


def possible_choices(board,l,c):
    line_numbers = board[l]
    column_numbers = board[:, c]
    square_numbers = np.reshape(board[
                                3 * (l // 3):3 * (l // 3) + 3,
                                3 * (c // 3):3 * (c // 3) + 3
                                ],
                                -1
                                )
    used_numbers = np.unique(np.append(np.append(line_numbers, column_numbers), square_numbers))
    used_numbers=np.delete(used_numbers, np.where(used_numbers == 0))
    return np.setdiff1d(np.array([i for i in range(1,10)]),used_numbers,assume_unique=False)


def solve(board):
    for i in range(100):
        for l in range(9):
            for c in range(9):
                board[l][c] = validate_cell(np.array(board), l, c)
        printboard(board)
        if np.count_nonzero(np.array(board) == 0) == 0:
            print("SUCCESS")
            break

board=read_sdk("2.sdk")
printboard(board)
#sol=list(initia_possible_solutions(board))
#printboard(sol)
#printboard(np.array(board)[:,0])
init=[]
for c in range(3,6):
    for l in range(6,9):
        if board[l][c]==0:
            print("{},{}->".format(l,c)+str(possible_choices(np.array(board),l,c)))

#print([(i if type(i) is not list) for i in board[0]])
#validate_cell(sol,0,1)
