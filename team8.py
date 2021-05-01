
import STcpClient
import random
import sys

# This Python file uses the following encoding: utf-8


'''
    輪到此程式移動棋子
    board : 棋盤狀態(list of list), board[l][i][j] = l layer, i row, j column 棋盤狀態(l, i, j 從 0 開始)
            0 = 空、1 = 黑、2 = 白、-1 = 四個角落
    is_black : True 表示本程式是黑子、False 表示為白子

    return Step
    Step : single touple, Step = (r, c)
            r, c 表示要下棋子的座標位置 (row, column) (zero-base)
'''
COLOR = 1
Depth_limit = 2
INFINITY = float('inf')
MINUS_INFINITY = float('-inf')
point = [0, 1, 10, 100, 5000]

# class state:
#     def __init__(self):
#         self.board = []
#         self.move = (-1,-1)


def inside(x, y):
    if(x < 0):
        return False
    if(y < 0):
        return False
    if(x > 5):
        return False
    if(y > 5):
        return False
    return True

def check_line_in_one_axis(board):
    line = 0
    score = 0
    info = [0, 0, 0] # blank, black, white
    for h in range(6):
        for i in range(6):
            for j in range(6):
                if(board[h][i][j] == COLOR):
                    info[COLOR] += 1
                    line += 1
                elif(board[h][i][j] == 0):
                    info[0] += 1
                    line += 1
                else:
                    info[COLOR] = 0
                    info[0] = 0
                    line = 0
                if(line == 4):
                    score += point[info[COLOR]]
                    info[board[h][i][j-3]] = max(info[board[h][i][j-3]]-1, 0)
                    line = max(line-1, 0)
            info[COLOR] = 0
            info[0] = 0
            line = 0
    for h in range(6):
        for j in range(6):
            for i in range(6):
                if(board[h][i][j] == COLOR):
                    info[COLOR] += 1
                    line += 1
                elif(board[h][i][j] == 0):
                    info[0] += 1
                    line += 1
                else:
                    info[COLOR] = 0
                    info[0] = 0
                    line = 0
                if(line == 4):
                    score += point[info[COLOR]]
                    info[board[h][i-3][j]] = max(info[board[h][i-3][j]]-1, 0)
                    line = max(line-1, 0)
            info[COLOR] = 0
            info[0] = 0
            line = 0
    for j in range(6):
        for i in range(6):
            for h in range(6):
                if(board[h][i][j] == COLOR):
                    info[COLOR] += 1
                    line += 1
                elif(board[h][i][j] == 0):
                    info[0] += 1
                    line += 1
                else:
                    info[COLOR] = 0
                    info[0] = 0
                    line = 0
                if(line == 4):
                    score += point[info[COLOR]]
                    info[board[h-3][i][j]] = max(info[board[h-3][i][j]]-1, 0)
                    line = max(line-1, 0)
            info[COLOR] = 0
            info[0] = 0
            line = 0
    return score

def check_line_in_two_axis(board):
    line = 0
    score = 0
    info = [0, 0, 0] # blank, black, white
    diagonal = [[0,2],[0,1],[0,0],[1,0],[2,0]]
    anti_diagonal = [[0,3],[0,4],[0,5],[1,5],[2,5]]
    for h in range(6):
        for i, j in diagonal:
            while inside(i, j):
                if(board[h][i][j] == COLOR):
                    info[COLOR] += 1
                    line += 1
                elif(board[h][i][j] == 0):
                    info[0] += 1
                    line += 1
                else:
                    info[COLOR] = 0
                    info[0] = 0
                    line = 0
                if(line == 4):
                    score += point[info[COLOR]]
                    info[board[h][i-3][j-3]] = max(info[board[h][i-3][j-3]]-1, 0)
                    line = max(line-1, 0)
                i += 1
                j += 1
            info[COLOR] = 0
            info[0] = 0
            line = 0
        for i, j in anti_diagonal:
            while inside(i, j):
                if(board[h][i][j] == COLOR):
                    info[COLOR] += 1
                    line += 1
                elif(board[h][i][j] == 0):
                    info[0] += 1
                    line += 1
                else:
                    info[COLOR] = 0
                    info[0] = 0
                    line = 0
                if(line == 4):
                    score += point[info[COLOR]]
                    info[board[h][i-3][j+3]] = max(info[board[h][i-3][j+3]]-1, 0)
                    line = max(line-1, 0)
                i += 1
                j -= 1
            info[COLOR] = 0
            info[0] = 0
            line = 0
    for i in range(6):
        for h, j in diagonal:
            while inside(h, j):
                if(board[h][i][j] == COLOR):
                    info[COLOR] += 1
                    line += 1
                elif(board[h][i][j] == 0):
                    info[0] += 1
                    line += 1
                else:
                    info[COLOR] = 0
                    info[0] = 0
                    line = 0
                if(line == 4):
                    score += point[info[COLOR]]
                    info[board[h-3][i][j-3]] = max(info[board[h-3][i][j-3]]-1, 0)
                    line = max(line-1, 0)
                h += 1
                j += 1
            info[COLOR] = 0
            info[0] = 0
            line = 0
        for h, j in anti_diagonal:
            while inside(h, j):
                if(board[h][i][j] == COLOR):
                    info[COLOR] += 1
                    line += 1
                elif(board[h][i][j] == 0):
                    info[0] += 1
                    line += 1
                else:
                    info[COLOR] = 0
                    info[0] = 0
                    line = 0
                if(line == 4):
                    score += point[info[COLOR]]
                    info[board[h-3][i][j+3]] = max(info[board[h-3][i][j+3]]-1, 0)
                    line = max(line-1, 0)
                h += 1
                j -= 1
            info[COLOR] = 0
            info[0] = 0
            line = 0
    for j in range(6):
        for h, i in diagonal:
            while inside(h, i):
                if(board[h][i][j] == COLOR):
                    info[COLOR] += 1
                    line += 1
                elif(board[h][i][j] == 0):
                    info[0] += 1
                    line += 1
                else:
                    info[COLOR] = 0
                    info[0] = 0
                    line = 0
                if(line == 4):
                    score += point[info[COLOR]]
                    info[board[h-3][i-3][j]] = max(info[board[h-3][i-3][j]]-1, 0)
                    line = max(line-1, 0)
                h += 1
                i += 1
            info[COLOR] = 0
            info[0] = 0
            line = 0
        for h, i in anti_diagonal:
            while inside(h, i):
                if(board[h][i][j] == COLOR):
                    info[COLOR] += 1
                    line += 1
                elif(board[h][i][j] == 0):
                    info[0] += 1
                    line += 1
                else:
                    info[COLOR] = 0
                    info[0] = 0
                    line = 0
                if(line == 4):
                    score += point[info[COLOR]]
                    info[board[h-3][i+3][j]] = max(info[board[h-3][i+3][j]]-1, 0)
                    line = max(line-1, 0)
                h += 1
                i -= 1
            info[COLOR] = 0
            info[0] = 0
            line = 0
    return score

def check_line_in_three_axis(board, is_black):

    return

def check_line_num(board):

    return check_line_in_one_axis(board) + check_line_in_two_axis(board)

def evaluation_funcion(board):

    return check_line_num(board)

def make_actions(board):

    step_list = []

    for i in range(6):
        for j in range(6):
            for h in range(6):
                if(board[h][i][j] == -1):
                    break
                if(board[h][i][j] == 0):
                    step_list.append((h,i,j))
                    break
    return step_list

def set_step(new_step, board, is_black, flag):
    h, i, j = new_step
    if(is_black):
        board[h][i][j] = 1
    else:
        board[h][i][j] = 2
    if(not flag):
        board[h][i][j] = 0

def check_game_over(board):

    total_pieces = 0

    for plane in board:
        for i in range( len(plane) ):
            for j in range( len( plane[i] ) ):

                if plane[i][j] == 1 or plane[i][j] == 2:
                    total_pieces += 1
                if total_pieces == 64:
                    return True


    return False

def alpha_beta_search(board, is_black, depth, alpha, beta):

    decision = {'move':(-1,-1),'value': 0}

    if depth == Depth_limit or check_game_over(board):
        decision['value'] =  evaluation_funcion(board)

        return decision

    if is_black:
        decision['value'] = MINUS_INFINITY

        for new_step in make_actions(board):
            set_step(new_step, board, is_black, True)
            new_decision = alpha_beta_search(board, False, depth + 1, alpha, beta)
            set_step(new_step, board, is_black, False)

            if new_decision['value'] > decision['value']:
                decision = new_decision
                decision['move'] = (new_step[1],new_step[2])

            if decision['value'] >= beta:
                return decision

            alpha = max(alpha, decision['value'])

        return decision

    else :
        decision['value'] = INFINITY

        for new_step in make_actions(board):
            set_step(new_step, board, is_black, True)
            new_decision = alpha_beta_search(board, False, depth + 1, alpha, beta)
            set_step(new_step, board, is_black, False)

            if new_decision['value'] < decision['value']:
                decision = new_decision
                decision['move'] = (new_step[1],new_step[2])

            if decision['value'] <= alpha:
                return decision

            beta = min(beta, decision['value'])

        return decision

def GetStep(board, is_black):
    if(is_black):
        COLOR = 1
    else:
        COLOR = 2
    best_dicision = alpha_beta_search(board, is_black, 0, MINUS_INFINITY, INFINITY)

    return best_dicision['move']
    """
    Example:

    x = random.randint(0, 5)
    y = random.randint(0, 5)
    return (x, y)
    """


while(True):
    (stop_program, id_package, board, is_black) = STcpClient.GetBoard()
    if(stop_program):
        break

    Step = GetStep(board, is_black)
    STcpClient.SendStep(id_package, Step)
