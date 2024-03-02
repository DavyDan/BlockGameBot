import numpy as np
from numpy import array as a
import matplotlib.pyplot as plt
import pandas as pd
# import logging
# logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
board = np.array(np.zeros((9,9)))
metalist = [board.copy()]

Score = 0
shapes = {"dot":a([[1]]),"square":a([[1,1],[1,1]]),"tlc":a([[1,1],[1,0]]),"trc":a([[1,1],[0,1]]),\
          "bl":a([[1,0],[1,1]]),"br":a([[0,1],[1,1]]),"v2":a([[1],[1]]),"v3":a([[1],[1],[1]]),\
          "v5":a([[1],[1],[1],[1],[1]]),"h2":a([[1,1]]),"h3":a([[1,1,1]]),"h5":a([[1,1,1,1,1]]),\
          "t":a([[1,1,1],[0,1,0],[0,1,0]]),"lt":a([[1,0,0],[1,1,1],[1,0,0]]),"rt":a([[0,0,1],[1,1,1],[0,0,1]]),\
          "ut":a([[0,1,0],[0,1,0],[1,1,1]]),"cross":a([[0,1,0],[1,1,1],[0,1,0]]),"l1":a([[1,0,0],[1,0,0],[1,1,1]]),\
          "l2":a([[1,1,1],[1,0,0],[1,0,0]]),"l3":a([[1,1,1],[0,0,1],[0,0,1]]),"l4":a([[0,0,1],[0,0,1],[1,1,1]]),\
          "lz":a([[1,0],[1,1],[0,1]]),"rz":a([[0,1],[1,1],[1,0]]),"ln":a([[1,1,0],[0,1,1]]),"rn":a([[0,1,1],[1,1,0]])}
          


def findspot(row,col,pc,board=board):
    pc = shapes[pc]
    prow, pcol = pc.shape
    if board[row:row+prow, col:col+pcol].any() == False and (row + prow <= 9 and col + pcol <= 9):
        x = score(clear=False) 
        return (row,col,x)
    else: return False

def placepiece(row,col,pc, newboard = board):
    pc = shapes.get(pc)
    prow, pcol = pc.shape
    board[row:row+prow, col:col+pcol] = pc
    metalist.append(newboard.copy())
    
    
    
def score(localscore = 0, clear=False, color=True):
    clearlist = []
    #score the columns
    for i in range(0,9):
        if board[:,i].all():
            clearlist.append(('column',i))
            localscore += 100
    #score the rows
    for i in range(0,9):
        if board[i].all():
            clearlist.append(('row',i))
            localscore += 200
    #score the squares
    for i in range(0,9,3):
        for j in range(0,9,3):
            if board[i:i+3,j:j+3].all():
                clearlist.append(('square',(i,j)))
                localscore += 300
    #cleartheboard
    if clear == True:
        if color == True: x = 0
        else: x = .5 
        for axis, loc in clearlist:
            if axis == 'column':
                board[:,loc] = x
            elif axis == 'row':
                board[loc, :] = x  
            elif axis == 'square':
                board[loc[0]:loc[0]+3,loc[1]:loc[1]+3] = x

    return localscore    

movelist = []
def piececheck(p):
    global positions
    positions = []
    swidth, sheight = shapes[p].shape
    for col in range(0,9-sheight):
        for row in range(0,9-swidth):
            positions.append(findspot(col,row,p))
    
    scorelist = pd.DataFrame(positions,columns=['Row','Column','Score'])
    move = scorelist.iloc[scorelist['Score'].idxmax()]
    movelist.append(tuple(move))
    placepiece(move[0],move[1],p)
    score(clear=True)
print(positions)

# testloop

# piececheck('h3')
# piececheck('h3')
# piececheck('h3')

piececheck('l2')
piececheck('l2')
piececheck('square')
piececheck('square')
piececheck('v2')




array_list = metalist
frame_index = 0
def showmeta(index):
    plt.clf()
    plt.imshow(array_list[frame_index], cmap='cool', interpolation='nearest')
    plt.title(f'Frame {frame_index + 1}/{len(array_list)}')
    plt.xticks(np.arange(-0.5, 9, 1),None)
    plt.yticks(np.arange(-0.5, 9, 1),None)
    plt.grid(which='both', color='grey', linestyle='-', linewidth=1)
    for i in range(0, 9, 3):
        plt.axhline(y=i - 0.5, color='black', linewidth=1.5)
        plt.axvline(x=i - 0.5, color='black', linewidth=1.5)
    plt.draw()
# Define function to update plot
def on_key(event):
    global frame_index

    if event.key == 'right':
        frame_index = min(frame_index + 1, len(array_list) - 1)
    elif event.key == 'left':
        frame_index = max(frame_index - 1, 0)

    #funcs to run 

    showmeta(frame_index)

showmeta(0)
print(movelist)
# Connect key press event to the figure
plt.connect('key_press_event', on_key)
plt.show()