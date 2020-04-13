import numpy as np
from math import floor

def read_board(path):
    l = []
    with open(path) as f:
        for line in f:
            t=[]
            for char in line:
                if char != '\n':
                    t.append(list([i for i in range(1,10)]) if char == '_' else int(char))
            l.append(t)
        return np.array(l)


def printboard(board):
    for item in board:
        for cell in item:
            print(cell if type(cell) in [int,np.int64] else '_'," ",end="")
        print("")


def print_situation(board):
    b_state=board_state(board)
    print("Board is {}% complete({}/81)".format(b_state[0],b_state[1]))
    for item in board:
        for cell in item:
            if type(cell) in [int,np.int64]:
                print("    " + str(cell) + "     ",end="")
            else:
                size=10-len(cell)
                print(" "*(size//2),end="")
                print("".join([str(i) for i in cell]),end="")
                print(" " * ((size // 2)+size%2), end="")
        print("")


def level1(board):
    for l in range(9):
        for c in range(9):
            if type(board[l][c]) in [int,np.int64]:

                remove_from_line(board,l,board[l][c])
                remove_from_column(board,c,board[l][c])
                remove_from_square(board,l,c,board[l][c])


def remove_from_cell(board,l,c,val):

    if type(board[l][c]) is list:
        if len(board[l][c]) == 1:
            board[l][c] = int(board[l][c][0])
            return
        #print(l, c, "->", board[l][c], "->", val)
        if val in board[l][c]:
            board[l][c].remove(val)
            if len(board[l][c])==1:
                board[l][c]=int(board[l][c][0])


def remove_from_line(board,l,val):
    for c in range(9):
        remove_from_cell(board,l,c,val)


def remove_from_column(board,c,val):
    for l in range(9):
        remove_from_cell(board,l,c,val)


def remove_from_square(board,l,c,val):
    for l1 in range(3):
        for c1 in range(3):
            remove_from_cell(board,3*(l//3)+l1,3*(c//3)+c1,val)


def write_in_cell(board,l,c,val):
    board[l][c]=int(val)
    remove_from_line(board, l, val)
    remove_from_column(board, c, val)
    remove_from_square(board, l, c, val)


def find_unique_in_lines2(board):
    for l in range(9):
        u,p=find_unique_in_group(board[l])
        for val,pos in zip(u,p):
            write_in_cell(board,l,pos,val)


def find_unique_in_columns2(board):
    for c in range(9):
        u,p=find_unique_in_group(board[:,c])
        for val,pos in zip(u,p):
            write_in_cell(board,pos,c,val)


def find_unique_in_group(group):
    """
    :param group: mus be a 1d list/array with 9 elements
    :return:
        list of uniques
    """
    unique=[]
    pos=[]
    for val in range(1,10):
        t = 0
        last_p=0
        if val not in group:
            for i in range(9):
                if type(group[i]) is list:
                    if val in group[i]:
                        t=t+1
                        last_p=i
            if t==1:
                unique.append(val)
                pos.append(last_p)
    return unique,pos


def find_unique_in_square2(board):
    for l in range(3):
        for c in range(3):
            u,p=find_unique_in_group(np.reshape(board[l*3:l*3+3,c*3:c*3+3],-1))
            for val,pos in zip(u,p):
                l1=pos//3
                c1=pos%3
                write_in_cell(board,l*3+l1,c*3+c1,val)


def find_pack_in_group(group):
    pos=list([list([]) for i in range(9)])
    for val in range(1,10):
        for i in range(9):
            if type(group[i]) is list:
                if val in group[i]:
                    pos[val-1].append(i)
    return pos


def find_duplicates(elements):
    ''' returns list of duplicates '''

    unique_elements = list(np.unique(np.array(elements)))
    #print(elements)
    duplicates = []

    for elem in unique_elements:
        if elements.count(elem)>1:
            duplicates.append(elem)
    if [] in duplicates:
        duplicates.remove([])
    return duplicates


def find_pack_in_squares(board):
    for l in range(3):
        for c in range(3):
            pos=find_pack_in_group(np.reshape(board[l*3:l*3+3,c*3:c*3+3],-1))
            for dup in find_duplicates(pos):
                opt=[]
                if len(dup)==2:
                    opt.append(pos.index(dup)+1)
                    opt.append(pos.index(dup,opt[0]) + 1)
                    for p in dup:
                        board[l*3+(p//3)][c*3+(p%3)]=list(opt)


def find_pack_in_lines(board):
    for l in range(9):
        pos=find_pack_in_group(board[l])
        for dup in find_duplicates(pos):
            opt=[]
            if len(dup)==2:
                opt.append(pos.index(dup)+1)
                opt.append(pos.index(dup,opt[0]) + 1)
                for p in dup:
                    board[l][p]=list(opt)


def find_pack_in_column(board):
    for c in range(9):
        pos=find_pack_in_group(board[:,c])
        #print(pos)
        for dup in find_duplicates(pos):
            opt=[]
            if len(dup)==2:
                opt.append(pos.index(dup)+1)
                opt.append(pos.index(dup,opt[0]) + 1)
                for p in dup:
                    board[p][c]=list(opt)
                    #print(p,c,"->",opt)


def board_state(board):
    cells_filled=0
    for l in range(9):
        for c in range(9):
            if type(board[l][c]) in [int,np.int64]:
                cells_filled+=1
    return floor(100*(cells_filled/81)),cells_filled


def solve(board):
    l_board=np.array(board)
    #print("11111")
    level1(board)
    #print_situation(board)
    for i in range(100):
        #print("2")
        find_unique_in_columns2(board)
        level1(board)
        #print_situation(board)
        #print("3")
        find_unique_in_lines2(board)
        level1(board)
        #print_situation(board)
        #print("4")
        find_unique_in_square2(board)
        level1(board)
        #print_situation(board)
        #print("5")
        find_pack_in_squares(board)
        level1(board)
        #print_situation(board)
        #print("6")
        find_pack_in_lines(board)
        level1(board)
        #print_situation(board)
        #print("7")
        find_pack_in_column(board)
        level1(board)
        #print_situation(board)
        if np.array_equal(board,l_board):
            print(i)
            break
        else:
            l_board=np.array(board)


def validate_cell(board,l,c,val):
    if val in board[l]:
        return False
    if val in board[:,c]:
        return False
    if val in np.reshape(board[3*(l//3):3*(l//3)+3,3*(c//3):3*(c//3)+3],-1):
        return False
    return True


def validate_board(board):
    result=np.array(list(range(1,10)))
    for l in board:
        if not np.array_equal(np.sort(l),result):
            print("l",l)
            return False
    for c in range(9):
        if not np.array_equal( np.sort(board[:,c]), result):
            print("c", c)
            return False
    for l in range(3):
        for c in range(3):
            if not np.array_equal(np.sort( np.reshape(board[l*3:l*3+3,c*3:c*3+3],-1)), result):
                print("s", l,c)
                return False
    return True


def brute_force(board,possibilities_board,coord,i=0):
    if len(coord)<=i:
        #print("Solved")
        return True
    next_coord=coord[i]
    possibilities = list(possibilities_board[next_coord[0]][next_coord[1]])
    #print(i,"-",next_coord,"-",len(possibilities),"-",possibilities)

    while True:
        if len(coord) <= i:
            #print("Solved")
            return True
        if len(possibilities) == 0:
            board[next_coord[0]][next_coord[1]]  = list(possibilities_board[next_coord[0]][next_coord[1]])
            #print("no possibilities")
            return False
        next_val=possibilities.pop()
        #print(next_val)
        if validate_cell(board,next_coord[0],next_coord[1],next_val):
            board[next_coord[0]][next_coord[1]] = next_val
            if brute_force(board,possibilities_board,coord,i+1):
                return True


def list_missing_cells(board):
    options=[[0 for i in range(9)] for i in range(9)]
    for l in range(9):
        for c in range(9):
            if type(board[l][c]) not in [int,np.int64]:
                options[l][c]=len(board[l][c])

    coord=[]
    for i in range(2, 10):
        for l in range(9):
            for c in range(9):
                if options[l][c]==i:
                    coord.append([l,c])
    return coord


if __name__=='__main__':
    import time
    start=time.time()
    board=read_board('examples/2.sdk')
    #print_situation(board)

    solve(board)


    print_situation(board)
    coord=list_missing_cells(board)
    brute_force(board,np.array(board),coord)
    print_situation(board)
    print(validate_board(board))
    print(time.time()-start)






