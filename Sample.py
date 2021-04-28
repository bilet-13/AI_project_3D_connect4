
import STcpClient
import random
import sys
import copy
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

Depth_limit = 4
INFINITY = float('inf')
MINUS_INFINITY = float('-inf')


# class state:
#     def __init__(self):
#         self.board = []
#         self.move = (-1,-1)


def check_middle(board , is_black):

    return

def check_line_in_one_axis(board, is_black):

    return

def check_line_in_two_axis(board, is_black):

    return

def check_line_in_three_axis(board, is_black):

    return

def check_line_num(board , is_black):

    return

def evaluation_funcion(board, is_black):
      
    return check_line(board, is_black) + 0.01*check_middle(board, is_black)
        
def make_actions(board):
    
    state_list = []
    index_dict = {}

    for l in range(len(boaard)):
        for i in range( len(board[l]) ):
            for j in range( len( board[l][i] ) ):
                
                if plane[i][j] == 0 and index_dict.get((i,j)) is None:
                    
                    new_board = copy.deepcopy(board)
                    if is_black:
                        new_board[l][i][j] == 1
                    else:
                        new_board[l][i][j] == 2

                    new_step = (i, j)
                    state_list.append( (new_board, new_step ))
                    index_dict[(i,j)] = True

    return state_list

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
        dicision['value'] =  evaluation_funcion(board,is_black)

        return dicision
    
    if is_black:
        decision['value'] = MINUS_INFINITY

        for (new_step, new_board) in make_actions(board, is_black):
            new_decision = alpha_beta_search(new_board, False, depth + 1, alpha, beta)

            if new_decision['value'] > decision['value']:
                decision = new_decision
                decision['move'] = new_step

            if decision['value'] >= beta:
                return decision

            alpha = max(alpha, decision['value'])
        
        return decision
    
    else :
        decision['value'] = INFINITY

        for state in make_actions(board, is_black):
            new_decision = alpha_beta_search(state.board, True, depth + 1, alpha, beta)
            move = state.move

            if new_decision['value'] < decision['value']:
                decision = new_decision
                decision['move'] = move

            if decision['value'] <= alpha:
                return decision

            beta = min(beta, decision['value'])
        
        return decision


def GetStep(board, is_black):

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
