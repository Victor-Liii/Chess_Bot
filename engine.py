import numpy
import chess
import chess.engine
import tensorflow


def minimax_eval(board, player):
    board3d = split_dims(board)
    board3d = numpy.expand_dims(board3d, 0)
    #print(model.predict(board3d)[0][0])
    #if player=="white":
    return model.predict(board3d)[0][0]
    #elif player=="black":
    #return 1-model.predict(board3d)[0][0]


def minimax(board, depth, alpha, beta, player, maximising):
    if depth == 0 or board.is_game_over():
        return minimax_eval(board,player)

    if maximising == True: # maximising score
        max_eval = -numpy.inf
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, player, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    elif maximising == False: # minimising score (invert as trained for white)
        min_eval = numpy.inf
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, player, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


# This is the actual function that gets the move from the neural network
def get_ai_move(board, depth, player):
    # White player tries to maximize score
    if player == "white":
      max_move = None
      # set max to -infinity
      max_eval = -numpy.inf

      for move in board.legal_moves:
          board.push(move)
          eval = minimax(board, depth - 1, -numpy.inf, numpy.inf, player, True)
          board.pop()
          if eval > max_eval:
              max_eval = eval
              max_move = move
    
      return max_move
    
    # Black player tries to minimize score
    elif player == "black":
      min_move = None
      # set min to infinity
      min_eval = numpy.inf

      for move in board.legal_moves:
          board.push(move)
          eval = minimax(board, depth - 1, -numpy.inf, numpy.inf, player)
          board.pop()
          if eval < min_eval:
              min_eval = eval
              min_move = move
      return min_move

def split_dims(board):
    # This is the 3D matrix
    # 14: 6 for white chess pieces, 6 for black chess pieces, 2 for valid attacks and moves for white and black
    # 8: 8 is the chess board size
    # Order is (pawns, knights, bishops, rooks, queen, king)

    board3d = numpy.zeros((14, 8, 8), dtype=numpy.int8)

    # Here we add the pieces's view on the matrix
    for piece in chess.PIECE_TYPES:
        for square in board.pieces(piece, chess.WHITE):
            idx = numpy.unravel_index(square, (8, 8))
            board3d[piece - 1][7 - idx[0]][idx[1]] = 1
        for square in board.pieces(piece, chess.BLACK):
            idx = numpy.unravel_index(square, (8, 8))
            board3d[piece + 5][7 - idx[0]][idx[1]] = 1

    # Add attacks and valid moves too
    # so the network knows what is being attacked
    aux = board.turn
    board.turn = chess.WHITE
    for move in board.legal_moves:
        i, j = square_to_index(move.to_square)
        board3d[12][i][j] = 1
    board.turn = chess.BLACK
    for move in board.legal_moves:
        i, j = square_to_index(move.to_square)
        board3d[13][i][j] = 1
    board.turn = aux

    return board3d

squares_index = {
  'a': 0,
  'b': 1,
  'c': 2,
  'd': 3,
  'e': 4,
  'f': 5,
  'g': 6,
  'h': 7
}


# example: h3 -> 17
def square_to_index(square):
    letter = chess.square_name(square)
    return 8 - int(letter[1]), squares_index[letter[0]]


    