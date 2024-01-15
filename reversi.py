class ReversiGame:
    def __init__(self):
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        self.board[3][3] = 'X'
        self.board[3][4] = 'O'
        self.board[4][3] = 'O'
        self.board[4][4] = 'X'
        self.current_player = 'X'
        self.player_name = None
        self.game_over = False

    def print_board(self):
        print("   A B C D E F G H")
        print("  -----------------")
        for i in range(8):
            print(f"{i + 1}| {' '.join(self.board[i])} |{i + 1}")
        print("  -----------------")
        print("   A B C D E F G H")

    def is_valid_move(self, row, col):
        if not (0 <= row < 8) or not (0 <= col < 8) or self.board[row][col] != ' ':
            return False

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        opponent = 'O' if self.current_player == 'X' else 'X'

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == opponent:
                while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == opponent:
                    r += dr
                    c += dc
                if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == self.current_player:
                    return True
        return False

    def make_move(self, row, col):
        if not self.is_valid_move(row, col):
            return "Ход невозможен"

        self.board[row][col] = self.current_player
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        opponent = 'O' if self.current_player == 'X' else 'X'

        for dr, dc in directions:
            r, c = row + dr, col + dc
            to_flip = []
            while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == opponent:
                to_flip.append((r, c))
                r += dr
                c += dc
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == self.current_player:
                for r, c in to_flip:
                    self.board[r][c] = self.current_player

        self.current_player = 'X' if self.current_player == 'O' else 'O'
        return self.get_next_move()

    def get_next_move(self):
        valid_moves = []
        for i in range(8):
            for j in range(8):
                if self.is_valid_move(i, j):
                    valid_moves.append((i, j))

        if not valid_moves:
            return self.end_game()

        # Оценка каждого доступного хода
        evaluated_moves = []
        for move in valid_moves:
            row, col = move
            score = self.evaluate_move(row, col)
            evaluated_moves.append((move, score))

        # Сортировка ходов по убыванию оценки (наилучший ход первым)
        sorted_moves = sorted(evaluated_moves, key=lambda x: x[1], reverse=True)

        return sorted_moves[0][0]

    def evaluate_move(self, row, col):
        opponent = 'O' if self.current_player == 'X' else 'X'
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        score = 0

        for dr, dc in directions:
            r, c = row + dr, col + dc
            to_flip = []
            while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == opponent:
                to_flip.append((r, c))
                r += dr
                c += dc
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == self.current_player:
                score += len(to_flip)

        return score

    def end_game(self):
        self.game_over = True
        count_x = sum(row.count('X') for row in self.board)
        count_o = sum(row.count('O') for row in self.board)
        if count_x > count_o:
            return f"Победил {self.player_name}" if self.player_name else "Победил игрок"
        elif count_x < count_o:
            return "Победил Бот"
        else:
            return "Ничья"

    def start_game(self):
        print("Реверси")
        self.player_name = input("Введите ваше имя: ")
        self.print_board()
        while not self.game_over:
            if self.current_player == 'X':
                move = input(f"{self.player_name}, введите ваш ход (например, 'A3'): ")
                col = ord(move[0].upper()) - 65
                row = int(move[1]) - 1
                result = self.make_move(row, col)
                if isinstance(result, list):
                    print("Доступные ходы: ", [f"{chr(move[0] + 65)}{move[1] + 1}" for move in result])
                else:
                    print(result)
            else:
                next_move = self.get_next_move()
                row, col = next_move
                print(f"Ход бота: {chr(col + 65)}{row + 1}")
                self.make_move(row, col)

            self.print_board()

        play_again = input("Хотите начать игру заново? (да/нет): ")
        if play_again.lower() in ['да', 'yes']:
            self.__init__()
            self.start_game()

# Создание экземпляра игры и запуск
game = ReversiGame()
game.start_game()
