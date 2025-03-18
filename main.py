from board import Board
from pieces import Piece, Pawn, Mimic

class Game:
    """
    Класс игры, где хранится информация об игре.
    """
    def __init__(self):
        self.board = Board()
        self.current_turn = 'white'
        self.move_count = 0
        self.move_history = []
        self.captured_piece = ''

    def hints(self, start, color):
        """
        Метод для подсказки куда можно сходить и какие фигуры можно съесть.

        Args:
            start (tuple): координаты, откуда ходят
            color (str): цвет, который ходит (нужно для подсветки угрожаемых фигур)
        """

        if self.board.get_piece(start):
            current_piece = self.board.get_piece(start)
            current_piece_moves = current_piece.get_possible_moves(self.board, start)

            if type(current_piece) == Pawn:
                for index, move in enumerate(current_piece_moves):
                    if move[1] == 'en':
                        current_piece_moves[index] = move[0]

            print('\n   A B C D E F G H')
            print(' +—————————————————+')
            for index0, row in enumerate(self.board.board):
                print(f'{8 - index0}|', end=' ')
                for index1, piece in enumerate(row):
                    if (index0, index1) in current_piece_moves:
                        print(f"\x1B[1;41m{piece if piece else '.'}\x1B[0m", end=' ')
                    elif (index0, index1) in Piece.under_attack(self.board, color):
                        print(f'\033[1;43m{piece if piece else '.'}\033[0m', end=' ')
                    else:
                        print(piece if piece else '.', end=' ')
                print(f'|{8 - index0}')
            print(' +—————————————————+')
            print('   A B C D E F G H')

    def start(self):
        """
        Начало игры, тут записаны проверки на ввод, передача хода другому игроку, цикл игры до ввода exit, возврат ходов.
        """
        while True:
            self.board.display(self.current_turn)
            print(f"Ход {'белых' if self.current_turn == 'white' else 'чёрных'}.")

            if self.board.find_king(self.current_turn) in Piece.under_attack(self.board, self.current_turn):
                print('Вам шах! Обезопасьте короля!')

            start = input('Введите координаты целевой фигуры: ').strip()
            if not start: continue
            if start == 'exit':
                print('Игра окончена!')
                break

            if start == 'undo':
                if not self.move_history:
                    print("Нет ходов для отмены.")
                    continue
                move_count, start, end, current_turn, captured_piece, en_passant = self.move_history.pop()
                print(f"Ход {'белых' if current_turn == 'white' else 'чёрных'}.")
                index_start = self.board.position_to_indices(start)
                index_end = self.board.position_to_indices(end)
                self.board.move_piece(index_end, index_start)

                if en_passant:
                    if current_turn == 'white':
                        self.board.place_piece((index_end[0] + 1, index_end[1]), captured_piece)
                    else: self.board.place_piece((index_end[0] - 1, index_end[1]), captured_piece)
                else: self.board.place_piece(index_end, captured_piece)

                self.move_count -= 1
                self.current_turn = 'black' if self.current_turn == 'white' else 'white'
                Piece.last_move = (self.board.position_to_indices(self.move_history[-1][1]),
                                   self.board.position_to_indices(self.move_history[-1][2]))
                continue


            if len(start) != 2 or start[0] not in 'abcdefgh' or start[1] not in '12345678':
                print("Некорректный ввод. Введите координаты в формате 'e2'.\n")
                continue

            index_start = self.board.position_to_indices(start)

            piece = self.board.get_piece(index_start)
            if not piece:
                print('На этой позиции нет фигуры.')
                continue

            print('Выбранная фигура:', piece)

            if piece.color != self.current_turn:
                print('Вы не можете ходить чужой фигурой.')
                continue

            self.hints(index_start, self.current_turn)
            print(f"Ход {'белых' if self.current_turn == 'white' else 'чёрных'}.")

            end = input('Введите целевые координаты хода: ').strip()
            if not end:
                continue

            if len(end) != 2 or end[0] not in 'abcdefgh' or end[1] not in '12345678':  # Проверка на корректный ввод
                print("Некорректный ввод. Введите координаты в формате 'e4'.\n")
                continue

            index_end = self.board.position_to_indices(end)

            if index_end in piece.get_possible_moves(self.board, index_start) or \
               (index_end, 'en') in piece.get_possible_moves(self.board, index_start):
                special_move = ''

                if (index_end, 'en') in piece.get_possible_moves(self.board, index_start):
                    special_move = 'en_passant'
                    if self.current_turn == 'white':
                        self.captured_piece = self.board.get_piece((index_end[0] + 1, index_end[1]))
                    else: self.captured_piece = self.board.get_piece((index_end[0] - 1, index_end[1]))
                else: self.captured_piece = self.board.get_piece(index_end)

                if type(piece) == Mimic:
                    self.board.board[index_start[0]][index_start[1]] = self.board.get_piece(index_end)
                    self.board.board[index_end[0]][index_end[1]] = piece
                else:
                    self.board.move_piece(index_start, index_end)

                if type(piece) == Pawn and (index_end[0] == 0 or index_end[0] == 7):
                    self.board.display(self.current_turn)
                    piece.transform(self.board, index_end)

                self.move_count += 1
                self.move_history.append([self.move_count, start, end, self.current_turn, self.captured_piece, special_move])
                Piece.last_move = (index_start, index_end)
                self.current_turn = 'black' if self.current_turn == 'white' else 'white'

            else:
                print('Недопустимый ход.')



game = Game()
game.start()