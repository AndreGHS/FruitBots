class Bot():



    def __init__(self):
        self.row = 0;
        self.column = 0;
        self.banana_count = 0;
        self.boardSize = 0;

    def move_up(self):
        if self.row - 1 >= 0:
            self.row -= 1;

    def move_down(self):
        if self.row + 1 <= self.boardSize:
            self.row += 1;

    def move_right(self):
        if self.column + 1 <= self.boardSize:
            self.column += 1;

    def move_left(self):
        if self.column - 1 >= 0:
            self.column -= 1;

    def catch_banana(self):
        self.banana_count += 1;

    def setBoard_size(self, size):
        self.boardSize = size;