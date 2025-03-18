from pieces import Piece, Pawn, Rook, Knight, Bishop, Queen, King, Mimic, Pegasus, Ninja

class Board:
    """
    Класс для поля.
    """
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.setup_check_board()

    def setup_check_board(self):
        """
        Расставляет фигуры на стартовые позиции на поле
        """
        for i in range(8):
            self.board[1][i], self.board[6][i] = Pawn('black'), Pawn('white')

        self.board[0][0], self.board[0][7] = Rook('black'), Rook('black')
        self.board[0][1], self.board[0][6] = Knight('black'), Knight('black')
        self.board[0][2], self.board[0][5] = Bishop('black'), Bishop('black')
        self.board[0][3], self.board[0][4] = Queen('black'), King('black')
        self.board[2][2], self.board[2][5] = Mimic('black'), Mimic('black')
        self.board[2][0], self.board[2][7] = Pegasus('black'), Pegasus('black')
        self.board[1][0], self.board[1][7] = Ninja('black'), Ninja('black')

        self.board[7][0], self.board[7][7] = Rook('white'), Rook('white')
        self.board[7][1], self.board[7][6] = Knight('white'), Knight('white')
        self.board[7][2], self.board[7][5] = Bishop('white'), Bishop('white')
        self.board[7][3], self.board[7][4] = Queen('white'), King('white')
        self.board[5][2], self.board[5][5] = Mimic('white'), Mimic('white')
        self.board[5][0], self.board[5][7] = Pegasus('white'), Pegasus('white')
        self.board[6][0], self.board[6][7] = Ninja('white'), Ninja('white')
        print()

    def display(self, color='white'):
        """
        Отображает доску, подсвечивая фигуры под боем жёлтым цветом.

        Args:
            :param color: (str) Цвет фигур, которых нужно подсветить
        """
        print('   A B C D E F G H')
        print(' +—————————————————+')
        for index0, row in enumerate(self.board):
            print(f'{8 - index0}|', end=' ')
            for index1, piece in enumerate(row):
                if (index0, index1) in Piece.under_attack(self, color):
                    print(f'\x1B[1;43m{piece if piece else '.'}\x1B[0m', end=' ')
                else:
                    print(f'{piece if piece else '.'}', end=' ')
            print(f'|{8 - index0}')
        print(' +—————————————————+')
        print('   A B C D E F G H')

    def get_piece(self, position):
        """
        Получение фигуры по позиции на доске.

        Args:
            :param position: (tuple) Позиция, откуда нужно получить фигуру

        :return: (object) Фигура на указанной позиции
        """
        if type(position[1]) == str:
            y, x = position[0]
        else: y, x = position
        return self.board[y][x] if self.is_valid_position(position) else None

    def place_piece(self, position, piece):
        """
        Размещение фигуры на доске.

        Args:
            :param position: (tuple) Позиция, куда нужно поставить фигуру
            :param piece: (object) Фигура, которую нужно поставить
        """
        y, x = position
        self.board[y][x] = piece

    def move_piece(self, start, end):
        """
        Перемещение фигуры с одной позиции на другую.

        Args:
            :param start: (tuple) Начальная позиция
            :param end: (tuple) Конечная позиция
        """
        start_y, start_x = start
        end_y, end_x = end

        if type(self.board[start_y][start_x]) == Pawn:
            if not self.board[end_y][end_x] and start_x != end_x:
                piece = self.board[start_y][start_x]
                self.board[end_y][end_x] = piece
                self.board[start_y][start_x] = None
                if self.get_piece(end).color == 'white':
                    self.board[end_y + 1][end_x] = None
                else: self.board[end_y - 1][end_x] = None
                return

        piece = self.get_piece(start)
        self.board[end_y][end_x] = piece
        self.board[start_y][start_x] = None

    def find_king(self, color):
        """
        Поиск позиции, на которой стоит король.

        :param color: (str) Цвет искомого короля
        :return: (int) Координаты короля
        """
        for index0, row in enumerate(self.board):
            for index1, piece in enumerate(row):
                if piece:
                    if type(piece) == King:
                        if piece.color == color:
                            return index0, index1

    @staticmethod
    def is_valid_position(position):
        """
        Проверка корректности введенных координат (не выходят ли они за пределы поля)

        Args:
            :param position: (tuple) координаты позиции

        :return: (bool) истина если координаты существуют в пределах доски и ложь в противном случае
        """
        if type(position[1]) == str:
            y, x = position[0]
        else: y, x = position
        return -1 < y < 8 and -1 < x < 8



    @staticmethod
    def position_to_indices(position):
        """
        Преобразование шахматной позиции в индексы массива.

        Args:
            :param position: (str) Позиция в формате 'e4'

        :return: (tuple) Индексы строки и столбца в формате (4, 4) - координата 'e4',
                 но в виде индексов вложенного списка
        """
        letter = position[0].lower()
        number = int(position[1])
        x = 8 - number
        y = ord(letter) - ord('a')
        return x, y

if __name__ == "__main__":
    board = Board()
    board.display()