class Move:
    """Представляет ход в игре. Хранит информацию о ходе для отмены."""
    def __init__(self, start_row, start_col, end_row, end_col, piece, captured_piece, jumped_piece_row=None, jumped_piece_col=None, became_queen=False):
        """Инициализация хода."""
        self.start_row = start_row
        self.start_col = start_col
        self.end_row = end_row
        self.end_col = end_col
        self.piece = piece
        self.captured_piece = captured_piece
        self.jumped_piece_row = jumped_piece_row
        self.jumped_piece_col = jumped_piece_col
        self.became_queen = became_queen

class Piece:
    """Базовый класс для фигур. Определяет общие свойства и методы."""
    def __init__(self, color, symbol):
        """Инициализация фигуры."""
        self.color = color
        self.symbol = symbol

    def __str__(self):
        """Возвращает строковое представление фигуры (символ)."""
        return self.symbol

    def possible_moves(self, board, start_row, start_col):
        """Возвращает список возможных ходов для фигуры. Реализуется в подклассах."""
        return []

    def is_valid_move(self, board, start_row, start_col, end_row, end_col):
        """Проверяет допустимость хода."""
        return (end_row, end_col) in self.possible_moves(board, start_row, start_col)

class Pawn(Piece):
    """Класс для пешки. Наследует от Piece и реализует логику движения."""
    def __init__(self, color):
        """Инициализация пешки."""
        super().__init__(color, "P" if color == "white" else "p")

    def possible_moves(self, board, start_row, start_col):
        """Возвращает список возможных ходов для пешки."""
        moves = []
        direction = -1 if self.color == "white" else 1
        new_row = start_row + direction

        if 0 <= new_row < 8 and not board.board[new_row][start_col]:
            moves.append((new_row, start_col))

        if (self.color == "white" and start_row == 6) or (self.color == "black" and start_row == 1):
            new_row = start_row + 2 * direction
            if not board.board[new_row][start_col] and not board.board[start_row + direction][start_col]:
                moves.append((new_row, start_col))

        for col_offset in [-1, 1]:
            new_col = start_col + col_offset
            new_row = start_row + direction
            if 0 <= new_row < 8 and 0 <= new_col < 8 and board.board[new_row][new_col] and board.board[new_row][new_col].color != self.color:
                moves.append((new_row, new_col))

        return moves

class Rook(Piece):
    """Класс для ладьи. Наследует от Piece и реализует логику движения."""
    def __init__(self, color):
        """Инициализация ладьи."""
        super().__init__(color, "R" if color == "white" else "r")

    def possible_moves(self, board, start_row, start_col):
        """Возвращает список возможных ходов для ладьи."""
        moves = []
        for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            for i in range(1, 8):
                new_row = start_row + direction[0] * i
                new_col = start_col + direction[1] * i

                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if not board.board[new_row][new_col]:
                        moves.append((new_row, new_col))
                    else:
                        if board.board[new_row][new_col].color != self.color:
                            moves.append((new_row, new_col))
                        break
                else:
                    break

        return moves

class Knight(Piece):
    """Класс для коня. Наследует от Piece и реализует логику движения."""
    def __init__(self, color):
        """Инициализация коня."""
        super().__init__(color, "N" if color == "white" else "n")

    def possible_moves(self, board, start_row, start_col):
        """Возвращает список возможных ходов для коня."""
        moves = []
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for move in knight_moves:
            new_row = start_row + move[0]
            new_col = start_col + move[1]

            if 0 <= new_row < 8 and 0 <= new_col < 8 and (not board.board[new_row][new_col] or board.board[new_row][new_col].color != self.color):
                moves.append((new_row, new_col))

        return moves

class Bishop(Piece):
    """Класс для слона. Наследует от Piece и реализует логику движения."""
    def __init__(self, color):
        """Инициализация слона."""
        super().__init__(color, "B" if color == "white" else "b")

    def possible_moves(self, board, start_row, start_col):
        """Возвращает список возможных ходов для слона."""
        moves = []
        for direction in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            for i in range(1, 8):
                new_row = start_row + direction[0] * i
                new_col = start_col + direction[1] * i

                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if not board.board[new_row][new_col]:
                        moves.append((new_row, new_col))
                    else:
                        if board.board[new_row][new_col].color != self.color:
                            moves.append((new_row, new_col))
                        break
                else:
                    break

        return moves

class Queen(Piece):
    """Класс для ферзя. Наследует от Piece и реализует логику движения."""
    def __init__(self, color):
        """Инициализация ферзя."""
        super().__init__(color, "Q" if color == "white" else "q")

    def possible_moves(self, board, start_row, start_col):
        """Возвращает список возможных ходов для ферзя. Ферзь ходит как ладья и слон."""
        return Rook(self.color).possible_moves(board, start_row, start_col) + Bishop(self.color).possible_moves(board, start_row, start_col)

class King(Piece):
    """Класс для короля. Наследует от Piece и реализует логику движения."""
    def __init__(self, color):
        """Инициализация короля."""
        super().__init__(color, "K" if color == "white" else "k")

    def possible_moves(self, board, start_row, start_col):
        """Возвращает список возможных ходов для короля."""
        moves = []
        king_moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for move in king_moves:
            new_row = start_row + move[0]
            new_col = start_col + move[1]

            if 0 <= new_row < 8 and 0 <= new_col < 8 and (not board.board[new_row][new_col] or board.board[new_row][new_col].color != self.color):
                moves.append((new_row, new_col))

        return moves

class Checker(Piece):
    """Класс для шашки. Наследует от Piece и реализует логику движения."""
    def __init__(self, color, is_queen = False):
        """Инициализация шашки."""
        super().__init__(color, "W" if color == "white" else "B")
        self.direction = -1 if color == "white" else 1
        self.is_queen = is_queen  # Flag to check if the checker is a queen
        if self.is_queen:
            self.symbol = "WQ" if color == "white" else "BQ"

    def possible_moves(self, board, start_row, start_col):
        """Возвращает список возможных ходов для шашки."""
        moves = []
        directions = [-1, 1] if self.is_queen else [self.direction]

        for direction in directions:
            for col_offset in [-1, 1]:
                new_col = start_col + col_offset
                new_row = start_row + direction
                if 0 <= new_col < 8 and 0 <= new_row < 8 and not board.board[new_row][new_col]:
                    moves.append((new_row, new_col))
        return moves

    def find_capture_moves(self, board, start_row, start_col):
        """Находит все ходы взятия для шашки."""
        capture_moves = []
        directions = [-1, 1] if self.is_queen else [self.direction]

        for direction in directions:
            for col_offset in [-1, 1]:
                new_col = start_col + col_offset
                new_row = start_row + direction
                jumped_row = start_row + 2 * direction
                jumped_col = start_col + 2 * col_offset

                if (0 <= new_row < 8 and 0 <= new_col < 8 and 0 <= jumped_row < 8 and 0 <= jumped_col < 8 and
                    board.board[new_row][new_col] and board.board[new_row][new_col].color != self.color and not board.board[jumped_row][jumped_col]):
                    capture_moves.append((jumped_row, jumped_col))
        return capture_moves

class Lancer(Piece):
    """Класс для Копейщика. Наследует от Piece и реализует логику движения."""
    def __init__(self, color): super().__init__(color, "L" if color == "white" else "l")
    def possible_moves(self, board, start_row, start_col):
        """Возвращает список возможных ходов для Копейщика."""
        moves = []
        direction = -1 if self.color == "white" else 1
        for i in range(1, 8):
            new_row = start_row + direction * i
            if 0 <= new_row < 8:
                if not board.board[new_row][start_col]:
                    moves.append((new_row, start_col))
                else:
                    if board.board[new_row][start_col].color != self.color:
                        moves.append((new_row, start_col))
                    break
            else:
                break
        return moves

class Assassin(Piece):
    """Класс для Ассасина. Наследует от Piece и реализует логику движения."""
    def __init__(self, color): super().__init__(color, "A" if color == "white" else "a")
    def possible_moves(self, board, start_row, start_col):
        """Возвращает список возможных ходов для Ассасина."""
        moves = []
        assassin_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for move in assassin_moves:
            new_row = start_row + move[0]
            new_col = start_col + move[1]
            if 0 <= new_row < 8 and 0 <= new_col < 8 and (not board.board[new_row][new_col] or board.board[new_row][new_col].color != self.color):
                moves.append((new_row, new_col))
        return moves

class Fortress(Piece):
    """Класс для Крепости. Наследует от Piece и реализует логику движения."""
    def __init__(self, color): super().__init__(color, "F" if color == "white" else "f")
    def possible_moves(self, board, start_row, start_col):
        """Возвращает список возможных ходов для Крепости."""
        moves = []
        fortress_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for move in fortress_moves:
            new_row = start_row + move[0]
            new_col = start_col + move[1]
            if 0 <= new_row < 8 and 0 <= new_col < 8 and (not board.board[new_row][new_col] or board.board[new_row][new_col].color != self.color):
                moves.append((new_row, new_col))
        for row in range(8):
            for col in range(8):
                if not board.board[row][col]:
                    moves.append((row, col))
        return moves

class Board:
    """Представляет шахматную/шашечную доску."""
    def __init__(self, game_type="chess", modified_chess=False):
        """Инициализация доски."""
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.game_type = game_type
        self.modified_chess = modified_chess
        self.setup_board()

    def setup_board(self):
        """Расстановка фигур."""
        if self.game_type == "chess":
            piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
            for i, piece_type in enumerate(piece_order):
                self.board[7][i] = piece_type("white")
                self.board[0][i] = piece_type("black")

            if self.modified_chess:
                pawn_replace = {1: Lancer, 4: Assassin, 6: Fortress}
                for i in range(8):
                    piece_type = pawn_replace.get(i, Pawn)
                    self.board[6][i] = piece_type("white")
                    self.board[1][i] = piece_type("black")
            else:
                for i in range(8):
                    self.board[6][i] = Pawn("white")
                    self.board[1][i] = Pawn("black")

        elif self.game_type == "checkers":
            for row in [0, 1, 2]:
                for col in range(8):
                    if (row + col) % 2 != 0: self.board[row][col] = Checker("black")
            for row in [5, 6, 7]:
                for col in range(8):
                    if (row + col) % 2 != 0: self.board[row][col] = Checker("white")

    def display(self, move_count, possible_moves=None, capture_moves=None, threatened_pieces=None, king_in_check=False):
        """Отображает доску в консоли."""
        print(f"Текущий ход: {move_count}")
        print("  a b c d e f g h")
        for row in range(8):
            print(8 - row, end=" ")
            for col in range(8):
                piece = self.board[row][col]
                if king_in_check and isinstance(piece, King) and piece.color == self.current_player: print("# ", end="")
                elif threatened_pieces and (row, col) in threatened_pieces: print("? ", end="")
                elif possible_moves and (row, col) in possible_moves: print("* ", end="")
                elif capture_moves and (row, col) in capture_moves: print("! ", end="")
                elif not piece: print(". ", end="")
                else: print(piece, end=" ")
            print(8 - row)
        print("  a b c d e f g h")

    def move_piece(self, start_row, start_col, end_row, end_col, jumped_piece_row=None, jumped_piece_col=None):
        """Перемещает фигуру с начальной позиции на конечную."""
        piece = self.board[start_row][start_col]
        captured_piece = self.board[end_row][end_col]

        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = None

        if jumped_piece_row is not None and jumped_piece_col is not None:
            self.board[jumped_piece_row][jumped_piece_col] = None

        return captured_piece

    def undo_move(self, move):
        """Отменяет ход."""
        self.board[move.start_row][move.start_col] = move.piece
        self.board[move.end_row][move.end_col] = move.captured_piece

        if move.jumped_piece_row and move.jumped_piece_col and self.game_type == "checkers":
            color = "black" if self.current_player == "white" else "white"
            self.board[move.jumped_piece_row][move.jumped_piece_col] = Checker(color)

        if move.became_queen:
            color = "black" if self.current_player == "white" else "white"
            self.board[move.start_row][move.start_col] = Checker(color)
            self.board[move.end_row][move.end_col] = None

class Game:
    """Управляет игровым процессом."""
    def __init__(self, game_type="chess", modified_chess=False):
        """Инициализация игры."""
        self.board = Board(game_type, modified_chess)
        self.current_player = "white"
        self.move_count = 1
        self.game_type = game_type
        self.modified_chess = modified_chess
        self.move_history = []

    def get_coordinates(self, position):
        """Преобразует шахматную нотацию (a2) в координаты доски (строка, столбец)."""
        if len(position) != 2 or not (0 <= (col := ord(position[0]) - ord("a")) < 8 and 0 <= (row := 8 - int(position[1])) < 8):
            return None
        return row, col

    def play(self):
        """Основной игровой цикл."""
        while True:
            threatened_pieces = self.find_threatened_pieces()
            king_in_check = self.is_king_in_check()

            self.board.display(self.move_count, possible_moves=None, capture_moves=None, threatened_pieces=threatened_pieces, king_in_check=king_in_check)
            print(f"Ход {self.move_count}. Ход {self.current_player}.")
            print("Введите 'отмена' для отмены хода или 'отмена N' для отмены N ходов.  Введите координаты фигуры (например, a2).")

            # 1. Выбор фигуры
            while True:
                start_position = input("Выберите фигуру для хода: ")

                if start_position == "отмена":
                    self.undo_last_move()
                    break
                elif start_position.startswith("отмена "):
                    try:
                        number_moves = int(start_position[7:])
                        self.undo_moves(number_moves)
                        break
                    except ValueError:
                        print("Неверный формат команды 'отмена'. Используйте 'отмена N', где N - целое число.")
                        continue

                start_coordinates = self.get_coordinates(start_position)
                if not start_coordinates:
                    print("Неверный формат позиции.  Пример: a2")
                    continue

                start_row, start_col = start_coordinates
                piece = self.board.board[start_row][start_col]
                if not piece:
                    print("На этой позиции нет фигуры.")
                    continue
                if piece.color != self.current_player:
                    print("Это не ваша фигура.")
                    continue

                # 2. Подсказка и отображение
                possible_moves = piece.possible_moves(self.board, start_row, start_col)
                capture_moves = piece.find_capture_moves(self.board, start_row, start_col) if self.game_type == "checkers" and isinstance(piece, Checker) else []

                if not possible_moves and not capture_moves and self.game_type == "chess":
                    print("У этой фигуры нет доступных ходов. Выберите другую фигуру.")
                    continue

                self.board.display(self.move_count, possible_moves, capture_moves, threatened_pieces, king_in_check)
                break

            if start_position == "отмена" or start_position.startswith("отмена "):
                continue

            # 3. Ввод целевой позиции
            while True:
                end_position = input("Введите целевую позицию: ")
                end_coordinates = self.get_coordinates(end_position)

                if not end_coordinates:
                    print("Неверный формат позиции.  Пример: a2")
                    continue

                end_row, end_col = end_coordinates
                jumped_piece_row = None
                jumped_piece_col = None
                captured_piece = None
                became_queen = False


                if self.game_type == "checkers" and isinstance(piece, Checker) and (end_row, end_col) in capture_moves:
                    jumped_piece_row = (start_row + end_row) // 2
                    jumped_piece_col = (start_col + end_col) // 2
                    captured_piece = self.board.board[jumped_piece_row][jumped_piece_col]

                elif self.board.board[end_row][end_col] and self.board.board[end_row][end_col].color != piece.color:
                  captured_piece = self.board.board[end_row][end_col]


                is_valid_move = (self.game_type == "checkers" and isinstance(piece, Checker) and (end_row, end_col) in capture_moves) or ((end_row, end_col) in possible_moves or (end_row, end_col) in capture_moves)

                if is_valid_move:
                    if self.game_type == "checkers" and isinstance(piece, Checker) and not piece.is_queen and (end_row == 0 or end_row == 7):
                        became_queen = True
                        piece = Checker(piece.color, True)
                        self.board.board[start_row][start_col] = None
                        self.board.board[end_row][end_col] = piece

                    captured_piece = self.board.move_piece(start_row, start_col, end_row, end_col, jumped_piece_row, jumped_piece_col)
                    move = Move(start_row, start_col, end_row, end_col, piece, captured_piece, jumped_piece_row, jumped_piece_col, became_queen)
                    self.move_history.append(move)
                    self.current_player = "black" if self.current_player == "white" else "white"
                    self.move_count += 1
                    break
                else:
                    print("Недопустимый ход.")
                    threatened_pieces = self.find_threatened_pieces()
                    king_in_check = self.is_king_in_check()
                    self.board.display(self.move_count, possible_moves, capture_moves, threatened_pieces, king_in_check)

    def find_threatened_pieces(self):
        """Находит все фигуры текущего игрока, находящиеся под боем."""
        threatened_pieces = []
        opponent_color = "black" if self.current_player == "white" else "white"
        for opponent_row in range(8):
            for opponent_col in range(8):
                opponent_piece = self.board.board[opponent_row][opponent_col]
                if opponent_piece and opponent_piece.color == opponent_color:
                    possible_opponent_moves = opponent_piece.possible_moves(self.board, opponent_row, opponent_col)
                    for row in range(8):
                        for col in range(8):
                            piece = self.board.board[row][col]
                            if piece and piece.color == self.current_player and not isinstance(piece, King) and (row, col) in possible_opponent_moves:
                                threatened_pieces.append((row, col))
        return threatened_pieces

    def is_king_in_check(self):
        """Проверяет, находится ли король под шахом."""
        king_position = next(((row, col) for row in range(8) for col in range(8) if isinstance(self.board.board[row][col], King) and self.board.board[row][col].color == self.current_player), None)
        if not king_position: return False
        king_row, king_col = king_position
        opponent_color = "black" if self.current_player == "white" else "white"
        return any(isinstance(self.board.board[row][col], Piece) and self.board.board[row][col].color == opponent_color and (king_row, king_col) in self.board.board[row][col].possible_moves(self.board, row, col) for row in range(8) for col in range(8))

    def undo_last_move(self):
        """Отменяет последний ход."""
        if self.move_history:
            move = self.move_history.pop()
            self.board.undo_move(move)
            self.current_player = "black" if self.current_player == "white" else "white"
            self.move_count -= 1
            print("Ход отменен.")
        else: print("История ходов пуста.")

    def undo_moves(self, number_moves):
        """Отменяет несколько ходов."""
        for _ in range(number_moves):
            if self.move_history: self.undo_last_move()
            else: print("История ходов пуста.")

if __name__ == "__main__":
    while True:
        game_type = input("Выберите игру (chess или checkers): ").lower()
        if game_type in ["chess", "checkers"]: break
        else: print("Неверный выбор.")

    modified_chess = False #Изначально ставим False
    if game_type == "chess":
        mod_str = input("Играть с новыми фигурами? (y/n): ").lower()
        modified_chess = mod_str == "y" #Если ввели y, то ставим True, иначе остаётся False.

    game = Game(game_type, modified_chess)
    game.play()
