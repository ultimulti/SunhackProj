'''
Grid display: [[Int]] (2-d array of integers)

For naming conventions and understanding of codes, 
9x9 board will be named as following. 
    a   b   c   d   e   f   g   h   i
0
1
2
3
4
5
6
7
8
'''
'''
Converting the given matrix to an input readable by sudokuSolver.
Return 2 dictionaries. 
'''
from itertools import product
import random as rd
# Solver for sudoku. Cred: Ali Assif
def solve_sudoku(size,grid):
    R, C = size
    N = R * C
    X = ([("rc", rc) for rc in product(range(N), range(N))] +
         [("rn", rn) for rn in product(range(N), range(1, N + 1))] +
         [("cn", cn) for cn in product(range(N), range(1, N + 1))] +
         [("bn", bn) for bn in product(range(N), range(1, N + 1))])
    Y = dict()
    for r, c, n in product(range(N), range(N), range(1, N + 1)):
        b = (r // R) * R + (c // C) # Box number
        Y[(r, c, n)] = [
            ("rc", (r, c)),
            ("rn", (r, n)),
            ("cn", (c, n)),
            ("bn", (b, n))]
    X, Y = exact_cover(X, Y)
    for i, row in enumerate(grid):
        for j, n in enumerate(row):
            if n:
                select(X, Y, (i, j, n))
    for solution in solve(X, Y, []):
        for (r, c, n) in solution:
            grid[r][c] = n
        yield grid

def exact_cover(X, Y):
    X = {j: set() for j in X}
    for i, row in Y.items():
        for j in row:
            X[j].add(i)
    return X, Y

def solve(X, Y, solution=[]):
    if not X:
        yield list(solution)
    else:
        c = min(X, key=lambda c: len(X[c]))
        for r in list(X[c]):
            solution.append(r)
            cols = select(X, Y, r)
            for s in solve(X, Y, solution):
                yield s
            deselect(X, Y, r, cols)
            solution.pop()

def select(X, Y, r):
    cols = []
    for j in Y[r]:
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].remove(i)
        cols.append(X.pop(j))
    return cols

def deselect(X, Y, r, cols):
    for j in reversed(Y[r]):
        X[j] = cols.pop()
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].add(i)
#End of Solver

#Create a sudoku grid with all 81 slots filled. 
def sudokuCreator():
    grid = []
    for i in range(9):
        grid.append([0]*9)
    return sudokuSolverLite(0, grid)[1]

#print out the grid
def printGrid(grid):
    for i in range(9):
        print(grid[i])
# fill a box with 9 values according to the rule. 
def fillBox(row, col, grid):
    unusedList = [k for k in range(1,10)]
    for i in range(3):
        for j in range(3):
            num = unusedList[rd.randrange(len(unusedList))]
            grid[i+row][j+col] = num
            unusedList.remove(num)
    return grid

#check if value 
def notInRow(ind, val, grid):
    for i in range(9):
        if grid[ind][i] == val:
            return False
    return True

def notInCol(ind, val, grid):
    for i in range(9):
        if grid[i][ind] == val:
            return False
    return True

def notInBox(row, col, val, grid):
    
    for i in range(3):
        for j in range(3):
            if grid[3*(row//3) + (i+row%3)%3][3*(col//3) + (j+col%3)%3] == val:
                return False
    return True

def safe(row, col, val, grid):
    return notInRow(row, val, grid) and \
            notInCol(col, val, grid) and \
            notInBox(row, col, val, grid)

def sudokuSolverLite(n, grid):

    flag = False
    '''
    for i in range(r, 9):
        for j in range(c, 9):
            if(grid[i][j] != 0):
                n += 1
            else:
                flag = True
                break
        if flag == True:
            break
    '''
    if (n >= 81):
        return (True, grid)
    while(grid[n//9][n%9] != 0):
        n+=1
        if (n >= 81):
            return (True, grid)

    r = n//9
    c = n%9
    available = []
    for val in range(1,10):
        if (safe(r,c, val, grid) == True):
            available.append(val)

    for i in range(len(available)):
        val = available[rd.randrange(len(available))]
        grid[r][c] = val
        if (sudokuSolverLite(n+1, grid)[0] == True):
            return (True, grid)
        available.remove(val)
    
    grid[r][c] = 0
    return (False, grid)

def gridRemover(grid, dif):
    i = 0
    contained = []
    r_rand = 0
    c_rand = 0
    while 2*i < dif:
        while True:
            r_rand = rd.randrange(9)
            c_rand = rd.randrange(9)
            if (r_rand, c_rand) not in contained and (c_rand, r_rand) not in contained:
                break
        
        grid[r_rand][c_rand] = 0
        grid[c_rand][r_rand] = 0
        i+= 1
    return grid

def checkValidSolution(grid):
    for i in range(9):
        for j in range(9):
            if (safe(i,j,grid[i][j],grid == False)):
                return False
    return True
# End of Solver. 
def main():
    grid = [[5, 3, 0, 0, 7, 0, 0, 0, 0],[6, 0, 0, 1, 9, 5, 0, 0, 0],[0, 9, 8, 0, 0, 0, 0, 6, 0],[8, 0, 0, 0, 6, 0, 0, 0, 3],[4, 0, 0, 8, 0, 3, 0, 0, 1],[7, 0, 0, 0, 2, 0, 0, 0, 6],[0, 6, 0, 0, 0, 0, 2, 8, 0],[0, 0, 0, 4, 1, 9, 0, 0, 5],[0, 0, 0, 0, 8, 0, 0, 7, 9]]

    printGrid(grid)
    print()

    grid = sudokuCreator()
    printGrid(grid)
    print()
    printGrid(gridRemover(grid, 68))
    for solution in solve_sudoku((3,3), grid):
        print(*solution, sep = "\n")    

if __name__ == "__main__":
    main()