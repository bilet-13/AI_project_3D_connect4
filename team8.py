
import STcpClient
#import random
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
COLOR = 0
OP_COLOR = 0
Depth_limit = 4
INFINITY = float('inf')
MINUS_INFINITY = float('-inf')
#black_point = [0, 1, 10, 100, 5000]
point = { 
    1:[0, 1, 10, 100, 5000], 2:[0, -1, -10, -100, -5000]
}
side_length = 6
remain_path_proportion = 2/3


def init_board(flag = 'game'):
    board = []
    #state = {'l':0,'i':0,"j":0}

    for l in range(6):
        board.append([])
        for i in range(6):
            board[l].append([])
    #print(board)
    #print(board)
    for l in range(6):
        for i in range(6):
            for j in range(6):

                if  flag == 'state':
                    state = {
                        'l': 0, 'i' : 0, "j" : 0, 
                        'dia_i&j' : 0,'anti_dia_i&j' : 0 ,
                        'dia_l&i' : 0, 'anti_dia_l&i' : 0, 
                        'dia_l&j' : 0, 'anti_dia_l&j' : 0 
                    }

                    board[l][i].append(state)
                else:
                    if  ( ( i == 0  or i == 5 ) and (j != 2 or j != 3) ) \
                        or ( ( i == 1 or i == 4 ) and ( j == 0 or j == 5) )  :
                        board[l][i].append(-1)
                    else:
                        board[l][i].append(0)
    return board

last_board = init_board()
state_board = init_board('state')
state_value_in_one = 0
state_value_in_two = 0

#************************************************************************init end
def reach_bound(x, y):

    if x == 0:
        return True

    elif y == 0 or y==5 :
        return True

    return False

def find_diagonal_started_point(x, y):

    while not reach_bound(x, y):

        x -= 1
        y -= 1
    
    return (x,y)

def find_anti_diagonal_started_point(x, y):

    while not reach_bound(x, y):

        x -= 1
        y += 1
    
    return (x,y)

def compare_with_last_board(board):

    for l in range(side_length):
        for i in range(side_length):
            for j in range(side_length):
                if last_board[l][i][j] != board[l][i][j]:

                    return (i,j)
    
    return None

def update_line_in_one_axis(board, cell_pos):

    global state_board

    line = 0
    score = 0
    info = [0, 0, 0] # blank, black, white
    cell_layer = cell_pos[0]
    cell_row = cell_pos[1]
    cell_column = cell_pos[2]
    difference = 0
    tmp_point = 0

    for j in range(6):
        if(board[cell_layer][cell_row][j] == COLOR):
            #print('find j '+str((cell_layer,cell_row,j)))
            info[COLOR] += 1
            line += 1
        elif(board[cell_layer][cell_row][j] == 0):
            info[0] += 1
            line += 1
        else:
            info[COLOR] = 0
            info[0] = 0
            line = 0
        if(line == 4):
            tmp_point = point[COLOR][info[COLOR]]
            score += tmp_point


            difference += tmp_point - state_board[cell_layer][cell_row][j-3]['j']
            state_board[cell_layer][cell_row][j-3]['j'] = tmp_point

            info[board[cell_layer][cell_row][j-3]] = max(info[board[cell_layer][cell_row][j-3]]-1, 0)
            line = max(line-1, 0)

    info[COLOR] = 0
    info[0] = 0
    line = 0

    
    for i in range(6):
        if(board[cell_layer][i][cell_column] == COLOR):
            #print('find i '+str((cell_layer,i,cell_column)))
            info[COLOR] += 1
            line += 1
        elif(board[cell_layer][i][cell_column] == 0):
            info[0] += 1
            line += 1
        else:
            info[COLOR] = 0
            info[0] = 0
            line = 0
        if(line == 4):
            tmp_point = point[COLOR][info[COLOR]]
            score += tmp_point

            difference += tmp_point - state_board[cell_layer][i-3][cell_column]['i']
            state_board[cell_layer][i-3][cell_column]['i'] = tmp_point

            info[board[cell_layer][i-3][cell_column]] = max(info[board[cell_layer][i-3][cell_column]]-1, 0)
            line = max(line-1, 0)

    info[COLOR] = 0
    info[0] = 0
    line = 0

    
    for h in range(6):
        if(board[h][cell_row][cell_column] == COLOR):
            #print('find h '+str((h,cell_row,cell_column)))
            info[COLOR] += 1
            line += 1
        elif(board[h][cell_row][cell_column] == 0):
            info[0] += 1
            line += 1
        else:
            info[COLOR] = 0
            info[0] = 0
            line = 0
        if(line == 4):
            tmp_point = point[COLOR][info[COLOR]]
            score += tmp_point
            #print('index '+str(h))
            #print('board '+str(state_board[1][cell_row][cell_column]['l']))

            difference += tmp_point - state_board[h-3][cell_row][cell_column]['l']
            index = h-3
            state_board[h-3][cell_row][cell_column]['l'] = tmp_point

            info[board[h-3][cell_row][cell_column]] = max(info[board[h-3][cell_row][cell_column]]-1, 0)
            line = max(line-1, 0)

    info[COLOR] = 0
    info[0] = 0
    line = 0

    global state_value_in_one

    state_value_in_one += difference

    return score

def update_line_in_two_axis(board, cell_pos):

    global state_board

    line = 0
    score = 0
    difference = 0
    tmp_point = 0

    info = [0, 0, 0] # blank, black, white
    cell_layer = cell_pos[0]
    cell_row = cell_pos[1]
    cell_column = cell_pos[2]

    diagonal = [[0,2],[0,1],[0,0],[1,0],[2,0]]
    anti_diagonal = [[0,3],[0,4],[0,5],[1,5],[2,5]]


    i, j = find_diagonal_started_point(cell_row, cell_column)

    while inside(i, j):
        # if board[h][i][j] == -1:
        #     print('errpr')
        #print((i,j))
        if(board[cell_layer][i][j] == COLOR):
            info[COLOR] += 1
            line += 1
        elif(board[cell_layer][i][j] == 0):
            info[0] += 1
            line += 1
        else:
            info[COLOR] = 0
            info[0] = 0
            line = 0
        if(line == 4):
            
            tmp_point = point[COLOR][info[COLOR]]
            score += tmp_point

            difference += tmp_point - state_board[cell_layer][i-3][j-3]['dia_i&j']
            state_board[cell_layer][i-3][j-3]['dia_i&j'] = tmp_point

            
            info[board[cell_layer][i-3][j-3]] = max(info[board[cell_layer][i-3][j-3]]-1, 0)
            line = max(line-1, 0)

        i += 1
        j += 1

    info[COLOR] = 0
    info[0] = 0
    line = 0

    anti_i, anti_j = find_anti_diagonal_started_point(cell_row, cell_column)
    
    while inside(anti_i, anti_j):
        if(board[cell_layer][anti_i][anti_j] == COLOR):
            info[COLOR] += 1
            line += 1
        elif(board[cell_layer][anti_i][anti_j] == 0):
            info[0] += 1
            line += 1
        else:
            info[COLOR] = 0
            info[0] = 0
            line = 0
        if(line == 4):
            tmp_point = point[COLOR][info[COLOR]]
            score += tmp_point

            difference += tmp_point - state_board[cell_layer][anti_i-3][anti_j-3]['anti_dia_i&j']
            state_board[cell_layer][anti_i-3][anti_j-3]['anti_dia_i&j'] = tmp_point

            info[board[cell_layer][anti_i-3][anti_j+3]] = max(info[board[cell_layer][anti_i-3][anti_j+3]]-1, 0)
            line = max(line-1, 0)


        anti_i += 1
        anti_j -= 1

    info[COLOR] = 0
    info[0] = 0
    line = 0


    h, j = find_diagonal_started_point(cell_layer, cell_column)

    while inside(h, j):
        if(board[h][cell_row][j] == COLOR):
            info[COLOR] += 1
            line += 1
        elif(board[h][cell_row][j] == 0):
            info[0] += 1
            line += 1
        else:
            info[COLOR] = 0
            info[0] = 0
            line = 0
        if(line == 4):
            tmp_point = point[COLOR][info[COLOR]]
            score += tmp_point

            difference += tmp_point - state_board[h-3][cell_row][j-3]['dia_l&j']
            state_board[h-3][cell_row][j-3]['dia_l&j'] = tmp_point

            info[board[h-3][cell_row][j-3]] = max(info[board[h-3][cell_row][j-3]]-1, 0)
            line = max(line-1, 0)

        h += 1
        j += 1

    info[COLOR] = 0
    info[0] = 0
    line = 0

    h, j = find_anti_diagonal_started_point(cell_layer, cell_column)

    while inside(h, j):
        if(board[h][cell_row][j] == COLOR):
            info[COLOR] += 1
            line += 1
        elif(board[h][cell_row][j] == 0):
            info[0] += 1
            line += 1
        else:
            info[COLOR] = 0
            info[0] = 0
            line = 0
        if(line == 4):
            tmp_point = point[COLOR][info[COLOR]]
            score += tmp_point

            difference += tmp_point - state_board[h-3][cell_row][j+3]['anti_dia_l&j']
            state_board[h-3][cell_row][j+3]['anti_dia_l&j'] = tmp_point

            info[board[h-3][cell_row][j+3]] = max(info[board[h-3][cell_row][j+3]]-1, 0)
            line = max(line-1, 0)

        h += 1
        j -= 1

    info[COLOR] = 0
    info[0] = 0
    line = 0


    h, i = find_diagonal_started_point(cell_layer, cell_row)

    while inside(h, i):
        if(board[h][i][cell_column] == COLOR):
            info[COLOR] += 1
            line += 1
        elif(board[h][i][cell_column] == 0):
            info[0] += 1
            line += 1
        else:
            info[COLOR] = 0
            info[0] = 0
            line = 0
        if(line == 4):
            tmp_point  = point[COLOR][info[COLOR]]
            score += tmp_point

            difference += tmp_point - state_board[h-3][i-3][cell_column]['dia_l&i']
            state_board[h-3][i-3][cell_column]['dia_l&i'] = tmp_point

            info[board[h-3][i-3][cell_column]] = max(info[board[h-3][i-3][cell_column]]-1, 0)
            line = max(line-1, 0)

        h += 1
        i += 1

    info[COLOR] = 0
    info[0] = 0
    line = 0

    h, i = find_anti_diagonal_started_point(cell_layer, cell_row)

    while inside(h, i):
        if(board[h][i][cell_column] == COLOR):
            info[COLOR] += 1
            line += 1
        elif(board[h][i][cell_column] == 0):
            info[0] += 1
            line += 1
        else:
            info[COLOR] = 0
            info[0] = 0
            line = 0
        if(line == 4):
            tmp_point  = point[COLOR][info[COLOR]]
            score += tmp_point

            difference += tmp_point - state_board[h-3][i+3][cell_column]['anti_dia_l&i']
            state_board[h-3][i+3][cell_column]['anti_dia_l&i'] = tmp_point

            info[board[h-3][i+3][cell_column]] = max(info[board[h-3][i+3][cell_column]]-1, 0)
            line = max(line-1, 0)

        h += 1
        i -= 1

    info[COLOR] = 0
    info[0] = 0
    line = 0

    global state_value_in_two
    state_value_in_two += difference

    return score


def update_state_board_and_value(board, step):

    i = step[0]
    j = step[1]
    layer = 0

    for h in range( side_length-1, -1, -1):
        if board[h][i][j] != 0:
            layer = h
            break


    update_line_in_one_axis(board, (layer, i, j))
    update_line_in_two_axis(board, (layer, i, j))

    return

def update_last_board(step, color):

    for l in range(side_length):

        if last_board[l][step[0]][step[1]] == 0:

            last_board[l][step[0]][step[1]] = color
            break

    return


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



def check_line_in_three_axis(board):
    line = 0
    score = 0
    info = [0, 0, 0] # blank, black, white
    
    diagonal = [[2,0], [1,1], [0,2]]
    anti_diagonal = [[0,3], [1,4], [2,5]]    
    diagonal_opposite = [[5,3], [4,4], [3,5]]
    anti_diagonal_opposite = [[3,0], [4,1], [5,2]]
    
    for start_h in range(3):
        for i, j in diagonal:
            h = start_h
            while inside(i, j):
                if (h > 5 or h < 0): 
                    break
                
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
                    info[board[h-3][i-3][j-3]] = max(info[board[h-3][i-3][j-3]]-1, 0)
                    line = max(line-1, 0)
                i += 1
                j += 1
                h += 1
            info[COLOR] = 0
            info[0] = 0
            line = 0
            
        for i, j in anti_diagonal:
            h = start_h
            while inside(i, j):
                if (h > 5 or h < 0): 
                    break
                
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
                    info[board[h-3][i-3][j+3]] = max(info[board[h-3][i-3][j+3]]-1, 0)
                    line = max(line-1, 0)
                i += 1
                j -= 1
                h += 1
            info[COLOR] = 0
            info[0] = 0
            line = 0
            
        for i, j in diagonal_opposite:
            h = start_h
            while inside(i, j):
                if (h > 5 or h < 0): 
                    break
                
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
                    info[board[h-3][i+3][j+3]] = max(info[board[h-3][i+3][j+3]]-1, 0)
                    line = max(line-1, 0)
                i -= 1
                j -= 1
                h += 1
            info[COLOR] = 0
            info[0] = 0
            line = 0
        
        for i, j in anti_diagonal_opposite:
            h = start_h
            while inside(i, j):
                if (h > 5 or h < 0): 
                    break
                
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
                    info[board[h-3][i+3][j-3]] = max(info[board[h-3][i+3][j-3]]-1, 0)
                    line = max(line-1, 0)
                i -= 1
                j += 1
                h += 1
            info[COLOR] = 0
            info[0] = 0
            line = 0
        
    return score


# def check_line_num(board):

#     return state_value_in_one + check_line_in_two_axis(board)
#     #return check_line_in_one_axis(board) + check_line_in_two_axis(board)

def Forward_pruning(board, step_list, is_black):

    min_val = INFINITY
    max_val =  MINUS_INFINITY
    bucket = {}
    return_list = []
    key_list = []

    for step in step_list:

        set_step(step, board, is_black, True)
        update_state_board_and_value(board, (step[1],step[2]) )

        val = evaluation_funcion(board)
        min_val = min(min_val , val)
        max_val = max(max_val, val)


        if bucket.get(val) is None:
            bucket[val] = []
            bucket[val].append(step)
            key_list.append(val)

        else:
            bucket[val].append(step)

        set_step(step, board, is_black, False)
        update_state_board_and_value(board, (step[1],step[2]) )

    if is_black:
        key_list.sort(reverse = True)
    else:
        key_list.sort()

    for i in range(len(key_list)):
        return_list.extend(bucket[key_list[i]])

        if len(return_list) >= (len(step_list) * remain_path_proportion) :
            break

    return return_list


def evaluation_funcion(board):

    return state_value_in_one + state_value_in_two

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

        new_step_list = make_actions(board)
        better_step_list = Forward_pruning(board, new_step_list, is_black)

        for new_step in better_step_list:

            set_step(new_step, board, is_black, True)
            update_state_board_and_value(board, (new_step[1],new_step[2]) )

            new_decision = alpha_beta_search(board, not is_black, depth + 1, alpha, beta)

            set_step(new_step, board, is_black, False)
            update_state_board_and_value(board, (new_step[1],new_step[2]) )

            if new_decision['value'] > decision['value']:
                decision = new_decision
                decision['move'] = (new_step[1],new_step[2])

            if decision['value'] >= beta:
                return decision

            alpha = max(alpha, decision['value'])

        return decision

    else :
        decision['value'] = INFINITY

        new_step_list = make_actions(board)
        better_step_list = Forward_pruning(board, new_step_list, is_black)

        for new_step in better_step_list:

            set_step(new_step, board, is_black, True)
            update_state_board_and_value(board, (new_step[1],new_step[2]) )

            new_decision =  alpha_beta_search(board, not is_black, depth + 1, alpha, beta)
            

            set_step(new_step, board, is_black, False)
            update_state_board_and_value(board, (new_step[1],new_step[2]) )
            # if COLOR == 2:
            #     print("value: "+str(decision['value'])+" step: "+str((new_step[1],new_step[2])) )

            if new_decision['value'] < decision['value']:
                decision = new_decision
                decision['move'] = (new_step[1],new_step[2])

            if decision['value'] <= alpha:
                return decision

            beta = min(beta, decision['value'])
        # if COLOR == 2:
        #     print("min_value: "+str(decision['value'])+" step: "+str((new_step[1],new_step[2])) )

        return decision

def GetStep(board, is_black):

    global COLOR
    global OP_COLOR

    if(is_black):
        COLOR = 1
        OP_COLOR = 2
    else:
        COLOR = 2
        OP_COLOR = 1

    step = compare_with_last_board( board)
    if step:
        update_last_board(step, OP_COLOR)
        update_state_board_and_value(board, step)

    best_dicision = alpha_beta_search(board, is_black, 0, MINUS_INFINITY, INFINITY)

    update_last_board(best_dicision['move'], COLOR)
    update_state_board_and_value(board, step)

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
