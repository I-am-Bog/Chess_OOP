class Piece:
    """
    Родительский класс для всех фигур.
    """

    last_move = []

    def __init__(self, color, symbol):
        """
        Args:
            :param color: (str) Цвет фигуры
            :param symbol: (str) Символ, который будет отображаться на доске
        """
        self.color = color
        self.symbol = symbol

    def __str__(self):
        """
        Рисует символ.

        :return: (str) Символ
        """
        return self.symbol

    def moves_p(self, board, start, direction):
        """
        Определение всех возможных ходов для пешки, но без учёта цвета фигур,
        то есть тут пешка может съесть свою фигуру.

        Args:
            :param board: (object) Текущее состояние доски
            :param start: (tuple) Позиция данной фигуры
            :param direction: (tuple) Направление хода, которое есть у фигуры (у пешки оно одно)

        :return: (list) Все возможные ходы без учёта цвета фигур
        """
        start_y, start_x = start
        moves = []

        if (board.is_valid_position((start_y + direction, start_x)) and
            not board.get_piece((start_y + direction, start_x))):
            moves.append((start_y + direction, start_x))

        if (self.color == 'white' and start_y == 6) or (self.color == 'black' and start_y == 1):
            if not (board.get_piece((start_y + direction * 2, start_x)) or
                    board.get_piece((start_y + direction, start_x))):
                moves.append((start_y + direction * 2, start_x))

        self.en_passant(board, start, direction, self.last_move, moves)

        # pawn_kill (Пешка кушает другую фигуру)
        for pawn_kills in [-1, 1]:
            kill_pos = (start_y + direction, start_x + pawn_kills)
            if board.is_valid_position(kill_pos):
                if board.get_piece(kill_pos):
                    moves.append(kill_pos)
        return moves

    def en_passant(self, board, start, direction, last_move, moves):
        """
        Дополнительный учёт "взятия на проходе" для пешки.
        Так как проверка довольно длинная, это реализовано как отдельный метод.

        Args:
            :param board: (object) Текущее состояние доски
            :param start: (tuple) Позиция данной фигуры
            :param direction: (tuple) Направления хода, которые есть у фигуры
            :param last_move: (tuple) Последний ход в формате (координаты начала, координаты конца)
            :param moves: (tuple) Все возможные ходы, без учёта цвета фигур

        :return: (tuple) тот же moves, но с учётом "взятия на проходе"
        """
        start_y, start_x = start

        if last_move:
            last_move_start = last_move[0]
            last_move_end = last_move[1]
            last_piece = board.get_piece(last_move_end)

            if type(last_piece) == Pawn and last_piece.color != self.color:
                if abs(last_move_end[0] - last_move_start[0]) == 2:
                    if abs(last_move_end[1] - start_x) == 1 and last_move_end[0] == start_y:
                        moves.append(((start_y + direction, last_move_end[1]), 'en'))
        return moves

    @staticmethod
    def moves_r_b_q(board, start, directions):
        """
        Определение всех возможных ходов для всех фигур, которые могут ходить бесконечно в своём направлении,
        (например: ладья, слон, ферзь, а также мимик и пегас)
        но без учёта цвета фигур, то есть тут можно съесть свою фигуру.

        Args:
            :param board: (object) Текущее состояние доски
            :param start: (tuple) Позиция данной фигуры
            :param directions: (tuple) Направления хода, которые есть у фигуры

        :return: (list) Все возможные ходы без учёта цвета фигур
        """
        start_y, start_x = start
        moves = []

        for dir_x, dir_y in directions:
            current_x, current_y = (start_y + dir_x, start_x + dir_y)
            while board.is_valid_position((current_x, current_y)):
                if board.get_piece((current_x, current_y)):
                    moves.append((current_x, current_y))
                    break
                moves.append((current_x, current_y))
                current_x += dir_x
                current_y += dir_y
        return moves

    @staticmethod
    def moves_n_k(board, start, directions):
        """
        Определение всех возможных ходов для всех фигур, которые могут ходить в определённом радиусе в своём направлении,
        (например: конь, король, а также ниндзя)
        но без учёта цвета фигур, то есть тут можно съесть свою фигуру.

        Args:
            :param board: (object) Текущее состояние доски
            :param start: (tuple) Позиция данной фигуры
            :param directions: (tuple) Направления хода, которые есть у фигуры

        :return: (list) Все возможные ходы без учёта цвета фигур
        """
        start_y, start_x = start
        moves = []

        for dir_x, dir_y in directions:
            current_pos = (start_y + dir_x, start_x + dir_y)
            if board.is_valid_position(current_pos):
                moves.append(current_pos)
        return moves

    def not_enemy(self, board, moves):
        """
        Проверка на цвет фигуры, то есть удаление из списка всех ходов возможность съесть свою фигуру.
        (можно было бы сделать проверку сразу, а не разделять на 2 метода, но так будет сложнее сделать мимика)

        Args:
            :param board: (object) Текущее состояние доски
            :param moves: (tuple) Все возможные ходы, без учёта цвета фигур

        :return: (tuple) отфильтрованный список ходов
        """
        return [move for move in moves if not board.get_piece(move) or board.get_piece(move).color != self.color]

    @staticmethod
    def get_all_possible_moves(board, color):
        """
        Получение всех ходов всех фигур данного цвета.

        Args:
            :param board: (object) Текущее состояние доски
            :param color: (str) Цвет, для которого нужно найти все ходы

        :return: (tuple) список всех ходов всех фигур
        """
        all_moves = []
        for index0, row in enumerate(board.board):
            for index1, piece in enumerate(row):
                if piece:
                    if piece.color != color:
                        if piece.get_possible_moves(board, (index0, index1)):
                            all_moves += piece.get_possible_moves(board, (index0, index1))
        return all_moves

    @staticmethod
    def under_attack(board, color):
        """
        Получение всех фигур, которые могут быть взяты во время следующего хода противника.

        Args:
            :param board: (object) Текущее состояние доски
            :param color: (str) Цвет, для которого нужно найти все фигуры под ударом

        :return: (tuple) список всех фигур под ударом
        """
        pieces_under_attack = []
        for move in Piece.get_all_possible_moves(board, color):
            if board.get_piece(move):
                if board.get_piece(move).color == color:
                    pieces_under_attack.append(move)
        return pieces_under_attack

class Pawn(Piece):
    """
    Класс для пешек.
    """
    def __init__(self, color):
        """
        Args:
            :param color: (str) Цвет фигуры (символ определяется относительно цвета)
        """
        super().__init__(color, 'P' if color == 'white' else 'p')
        self.direction = -1 if self.color == 'white' else 1

    def get_possible_moves(self, board, start):
        """
        Определение всех возможных ходов для данной пешки.

        Args:
            :param board: (object) Текущее состояние доски
            :param start: (tuple) Позиция данной пешки

        :return: (list) Все возможные ходы для данной пешки
        """
        return self.not_enemy(board, self.moves_p(board, start, self.direction))

    def transform(self, board, end):
        """
        Замена пешки на другую фигуру по достижению края поля,
        ничего не возвращает, а просто ставит выбранную фигуру на место пешки.

        Args:
            :param board: (object) Текущее состояние доски
            :param end: (tuple) Позиция данной пешки
        """
        chosen_piece = input('Пешка дошла до края поля! Выберите фигуру для замены: ').upper()
        if chosen_piece in ['R', 'B', 'Q', 'N']:
            match chosen_piece:
                case 'R': board.place_piece(end, Rook(self.color))
                case 'B': board.place_piece(end, Bishop(self.color))
                case 'Q': board.place_piece(end, Queen(self.color))
                case 'N': board.place_piece(end, Knight(self.color))



class Rook(Piece):
    """
    Класс для ладьи.
    """
    def __init__(self, color):
        super().__init__(color, 'R' if color == 'white' else 'r')
        self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def get_possible_moves(self, board, start):
        return self.not_enemy(board, self.moves_r_b_q(board, start, self.directions))



class Bishop(Piece):
    """
    Класс для слона.
    """
    def __init__(self, color):
        super().__init__(color, 'B' if color == 'white' else 'b')
        self.directions = [(-1, -1), (1, 1), (-1, 1), (1, -1)]

    def get_possible_moves(self, board, start):
        return self.not_enemy(board, self.moves_r_b_q(board, start, self.directions))



class Queen(Piece):
    """
    Класс для королевы.
    """
    def __init__(self, color):
        super().__init__(color, 'Q' if color == 'white' else 'q')
        self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]

    def get_possible_moves(self, board, start):
        return self.not_enemy(board, self.moves_r_b_q(board, start, self.directions))



class Knight(Piece):
    """
    Класс для коня.
    """
    def __init__(self, color):
        super().__init__(color, 'N' if color == 'white' else 'n')
        self.directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

    def get_possible_moves(self, board, start):
        return self.not_enemy(board, self.moves_n_k(board, start, self.directions))



class King(Piece):
    """
    Класс для короля.
    """
    def __init__(self, color):
        super().__init__(color, 'K' if color == 'white' else 'k')
        self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]

    def get_possible_moves(self, board, start):
        return self.not_enemy(board, self.moves_n_k(board, start, self.directions))



class Mimic(Piece):
    """
    Класс для 'мимика'.
    Мимик - новая фигура со сложным поведением. Сам по себе ходить не умеет, но если в радиусе 1 клетки находится другая фигура
    (даже вражеская), мимик перенимает её ходы. Если рядом с мимиком находятся разные фигуры, то он сможет ходить как смесь этих фигур.
    Мимик не атакует, то есть с его помощью нельзя съесть вражескую фигуру, а меняется местами с выбранной фигурой.
    """
    def __init__(self, color):
        super().__init__(color, 'M' if color == 'white' else 'm')
        self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]

    def get_possible_moves(self, board, start):
        near_pieces = self.find_nears(board, self.directions, start)
        moves = []

        for piece in near_pieces:
            if type(piece) in [Rook, Bishop, Queen, Pegasus]:
                for move in piece.moves_r_b_q(board, start, piece.directions):
                    if move not in moves:
                        moves.append(move)
            elif type(piece) in [Knight, King]:
                for move in piece.moves_n_k(board, start, piece.directions):
                    if move not in moves:
                        moves.append(move)
            elif type(piece) == Pawn:
                for move in piece.moves_p(board, start, piece.direction):
                    if move not in moves:
                        moves.append(move)
        return moves

    @staticmethod
    def find_nears(board, directions, start):
        """
        Поиск находящихся рядом фигур в заданном радиусе.

        Args:
            :param board: (object) Текущее состояние доски
            :param directions: (tuple) Направления поиска
            :param start: (tuple) Позиция фигуры, для которой ищем рядом стоящие фигуры
        """
        near_pieces = []
        start_x, start_y = start
        for direction in directions:
            dir_x, dir_y = direction
            if board.get_piece((start_x + dir_x, start_y + dir_y)):
                near_pieces.append(board.get_piece((start_x + dir_x, start_y + dir_y)))
        return near_pieces



class Pegasus(Piece):
    """
    Класс для пегаса.
    Пегас - новая фигура. Ходит как конь, но бесконечно в выбранном направлении, если на пути нет фигур.
    """
    def __init__(self, color):
        super().__init__(color, 'G' if color == 'white' else 'g')
        self.directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

    def get_possible_moves(self, board, start):
        return self.not_enemy(board, self.moves_r_b_q(board, start, self.directions))



class Ninja(Piece):
    """
    Класс для ниндзя.
    Ниндзя - новая фигура. Ходит через 1 клетку вертикально, горизонтально и диагонально,
    в общем как король, только пропускает клетку перед собой.
    """
    def __init__(self, color):
        super().__init__(color, 'J' if color == 'white' else 'j')
        self.directions = [(2, 0), (-2, 0), (0, 2), (0, -2), (2, 2), (2, -2), (-2, 2), (-2, -2)]

    def get_possible_moves(self, board, start):
        return self.not_enemy(board, self.moves_n_k(board, start, self.directions))