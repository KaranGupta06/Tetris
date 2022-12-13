import multiprocessing as mp
from msvcrt import getch
from copy import deepcopy
from time import sleep
import random
import os

blocks = [
    [[0, 0, 0],
     [1, 1, 1],
     [0, 1, 0]],

    [[0, 0, 0],
     [0, 1, 1],
     [0, 1, 1]],

    [[0, 0, 0],
     [0, 1, 1],
     [1, 1, 0]],

    [[0, 0, 0],
     [1, 1, 0],
     [0, 1, 1]],

    [[0, 0, 0],
     [1, 1, 1],
     [1, 0, 0]],

    [[0, 0, 0],
     [1, 1, 1],
     [0, 0, 1]],
    
    [[0, 1, 0, 0],
     [0, 1, 0, 0],
     [0, 1, 0, 0],
     [0, 1, 0, 0]]
]

game_board = [[0]*8 for _ in range(20)]
block = random.choice(blocks)
x, y = 2, 0

def display():
    global x, y, block

    temp_board = deepcopy(game_board)

    for i in range(len(block)):
        for j in range(len(block)):
            if block[i][j]:
                temp_board[y + j][x + i] = "#"

    os.system("cls")
    for i in temp_board:
        for j in i:
            if j == 0:
                print(".", end=" ")
            else:
                print("#", end=" ")
        print()

def update(inp):
    global x, y, block, game_board

    if inp == 80 and can_move(block, 0, 1):                          #down
        y += 1
    elif inp == 75 and can_move(block, -1, 0):                       #left
        x -= 1
    elif inp == 77 and can_move(block, 1, 0):                        #right
        x += 1
    elif inp == 122 and can_move(rot := rotate_block("r"), 0, 0):    #z
        block = rot
    elif inp == 120 and can_move(rot := rotate_block("l"), 0, 0):    #x
        block = rot

    if inp == 80 and not can_move(block, 0, 1):
        for i in range(len(block)):
            for j in range(len(block)):
                if block[i][j]:
                    game_board[y + j][x + i] = "#"

        for i, j in enumerate(game_board):
            if all(j):
                game_board.pop(i)
                game_board.insert(0, [0 for _ in range(8)])

        block = random.choice(blocks)
        x, y = 2, 0
    
def can_move(block, dx, dy) -> bool:
    for i in range(len(block)):
        for j in range(len(block)):
            if block[i][j]:
                if not (x + i + dx) in range(8) or not (y + j + dy) in range(20) or\
                    game_board[y + j + dy][x+ i + dx]:
                    return False
    return True

def rotate_block(direction: str) -> list:
    size = len(block)
    rotated_struc = [[0]*size for _ in range(size)]

    for i in range(size):
        for j in range(size):
            if direction == "r":
                rotated_struc[j][size - 1 - i] = block[i][j]
            else:
                rotated_struc[size - 1 - i][j] = block[j][i]
    
    return rotated_struc


def user_input(queue):
    while True:
        queue.put(ord(getch()))

def level_rate(queue, tick_rate):
    while True:
        sleep(tick_rate)
        queue.put(80)

def gameloop(queue):
    while True:
        if not queue.empty():
            update(queue.get())
            display()
            
def main():
    Queue = mp.Queue()

    p1 = mp.Process(target=user_input, args=[Queue])
    p2 = mp.Process(target=gameloop, args=[Queue])
    p3 = mp.Process(target=level_rate, args=[Queue, 0.5])

    p1.start()
    p2.start()
    p3.start()

if __name__ == "__main__":
    main()