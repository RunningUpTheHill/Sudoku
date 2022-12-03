import pygame
from sudoku_generator import *

width, height = 675, 750
black_color = (0, 0, 0)
gray_color = (128, 128, 128)
corn_silk = (238, 232, 205)
red_color = (255, 0, 0)
white_color = (255, 255, 255)
yellow_color = (255, 255, 0)
emerald = (0, 134, 139)
turquoise = (64, 224, 208)
menu_green = (148, 171, 67)
darker_green = (123, 144, 56)
aqua_marine = (127, 255, 212)
brown_color = (139, 35, 35)
crimson_color = (220, 20, 60)
maroon = (128, 0, 0)
orange = (255, 97, 3)
dark = (3, 3, 3)
cell_size = 75
line_width1 = 6
line_width2 = 2
rows = 9
cols = 9


class Cell:
    def __init__(self, value, row, col, width, height):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.sketch_val = None

    def set_value(self, val):
        self.value = val

    def set_sketch_value(self, val):
        self.sketch_val = val

    def draw(self, screen):
        if self.value != 0:
            font = pygame.font.Font(None, 80)
            num_surf = font.render(str(self.value), True, black_color)
            num_rect = num_surf.get_rect(center=(cell_size * self.col + cell_size // 2,
                                                 cell_size * self.row + cell_size // 2))
            screen.blit(num_surf, num_rect)


class Board:
    def __init__(self, rows, cols, width, height, screen, difficulty):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        if self.difficulty == "Easy":
            self.val = 30
        elif self.difficulty == 'Medium':
            self.val = 40
        else:
            self.val = 50
        self.tupl_board = generate_sudoku(9, self.val) #Generates a tuple that contains the ready board and correct solution
        self.board = self.tupl_board[0]
        self.correct = self.tupl_board[1]
        self.cell = [[Cell(self.board[i][j], i, j, cell_size, cell_size) for j in range(cols)] for i in range(rows)]

    def draw(self):
        for r in range(2):
            pygame.draw.line(
                screen,
                black_color,
                (0, r * 9 * cell_size),
                (width, r * 9 * cell_size),
                line_width1
            )

        for b in range(2):
            pygame.draw.line(
                screen,
                black_color,
                (b * 9 * cell_size, 0),
                (b * 9 * cell_size, 9 * cell_size),
                line_width1
            )

        for i in range(1, 4):
            pygame.draw.line(
                screen,
                black_color,
                (0, 3 * i * cell_size),
                (width, 3 * i * cell_size),
                line_width1
            )

        for c in range(1, 3):
            pygame.draw.line(
                screen,
                black_color,
                (3 * c * cell_size, 0),
                (3 * c * cell_size, height - cell_size),
                line_width1
            )

        for h in range(1, 9):
            pygame.draw.line(
                screen,
                black_color,
                (0, h * cell_size),
                (width, h * cell_size),
                line_width2
            )

        for v in range(1, 9):
            pygame.draw.line(
                screen,
                black_color,
                (v * cell_size, 0),
                (v * cell_size, height - cell_size),
                line_width2
            )

        for i in range(self.rows):
            for j in range(self.cols):
                self.cell[i][j].draw(screen)

    def select(self, row, col):
        pos = pygame.mouse.get_pos()
        if pos[1] <= 9 * cell_size:
            for i in range(2):
                pygame.draw.line(
                    screen,
                    red_color,
                    ((col + i) * cell_size, row * cell_size),
                    ((col + i) * cell_size, (row + 1) * cell_size),
                    line_width2
                )

            for j in range(2):
                pygame.draw.line(
                    screen,
                    red_color,
                    (col * cell_size, (row + j) * cell_size),
                    ((col + 1) * cell_size, (row + j) * cell_size),
                    line_width2
                )

    def click(self):
        click_pos = pygame.mouse.get_pos()
        x, y = click_pos[0] // cell_size, click_pos[1] // cell_size
        if x <= width:
            return y, x
        return None

    def clear(self):
        self.value = 0

    def sketch(self, value):
        font = pygame.font.Font(None, 5)

        sketch_num_surf = font.render(Cell.sketch_val, True, gray_color)

    def place_number(self, value):
        font = pygame.font.Font(None, 12)
        num_surf = font.render(Cell.value, True, black_color)

    def reset_to_original(self):
        self.board = self.tupl_board[0]

    def is_full(self):
        count = 0
        for row in self.board:
            for col in row:
                if col != 0:
                    count += 1
        if count == 81:
            return True
        else:
            return False

    def update_board(self):
        pass

    def find_empty(self):
        for n in range(rows):
            for m in range(cols):
                if self.board[n][m] != self.correct[n][m]:
                    return (n, m)

    def check_board(self):
        for n in range(rows):
            for m in range(cols):
                if self.board[n][m] != self.correct[n][m]:
                    return False
        else:
            return True


def menu_options():
    font_2 = pygame.font.Font(None, 50)
    menu_bg = pygame.image.load("sudokustartscreen.jpg").convert()
    screen.blit(menu_bg, (-65, 0))
    prompt_text = "Select Game Mode"
    prompt_surf = font_2.render(prompt_text, True, menu_green)
    prompt_rect = prompt_surf.get_rect(center=(width // 3.35, 523))
    screen.blit(prompt_surf, prompt_rect)


class Button():        # inspired by https://www.youtube.com/watch?v=4_9twnEduFA&ab_channel=TechWithTim
    def __init__(self, color, x, y, width, height, text):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, screen, outline, font_size=70):
        pygame.draw.rect(screen, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)
        font = pygame.font.Font(None, font_size)
        text = font.render(self.text, True, white_color)
        screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y +
                           (self.height / 2 - text.get_height() / 2)))

    def click(self, pos):
        if ((pos[0] > self.x) and (pos[0] < self.x + self.width)) and \
                ((pos[1] > self.y) and (pos[1] < self.y + self.height)):
            return True
        return False


def interactive_button(bool):
    if bool is True:
        easy_button.draw(screen, red_color)
        medium_button.draw(screen, red_color)
        hard_button.draw(screen, red_color)


def option_interactive(bol):
    if bol is True:
        reset_button.draw(screen, black_color, 40)
        restart_button.draw(screen, crimson_color, 40)
        quit_button.draw(screen, emerald, 40)


if __name__ == "__main__":
    pygame.init()

    while True:

        double_break = False

        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sudoku")
        menu_options()
        board_easy = Board(rows, cols, width, height, screen, "Easy")
        board_medium = Board(rows, cols, width, height, screen, "Medium")
        board_hard = Board(rows, cols, width, height, screen, "Hard")
        easy_button = Button(menu_green, 50, 610, 120, 80, "Easy")
        medium_button = Button(menu_green, 240, 610, 185, 80, "Medium")
        hard_button = Button(menu_green, 500, 610, 120, 80, "Hard")
        reset_button = Button(turquoise, 150, 690, 80, 50, "Reset")
        restart_button = Button(black_color, 290, 690, 100, 50, "Restart")
        quit_button = Button(maroon, 450, 690, 80, 50, "Quit:(")

        game_over = False
        booly, bol = True, False
        game_on = False
        cur_board = None

        while True:
            if double_break: #Breaks again if double break intended
                break

            for event in pygame.event.get():
                position = pygame.mouse.get_pos()
                interactive_button(booly)
                option_interactive(bol)
                pygame.display.update()

                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if game_on:
                        y, x = cur_board.click()
                        cur_board.draw()
                        cur_board.select(y, x)

                    if easy_button.click(position):
                        booly, bol = False, True
                        easy_button = Button(menu_green, 0, 0, 0, 0, "Easy")
                        medium_button = Button(menu_green, 0, 0, 0, 0, "Medium")
                        hard_button = Button(menu_green, 0, 0, 0, 0, "Hard")
                        screen.fill(corn_silk)
                        board_easy.draw()
                        cur_board = board_easy
                        game_on = True

                    elif medium_button.click(position):
                        booly, bol = False, True
                        easy_button = Button(menu_green, 0, 0, 0, 0, "Easy")
                        medium_button = Button(menu_green, 0, 0, 0, 0, "Medium")
                        hard_button = Button(menu_green, 0, 0, 0, 0, "Hard")
                        screen.fill(corn_silk)
                        board_medium.draw()
                        cur_board = board_medium
                        game_on = True

                    elif hard_button.click(position):
                        booly, bol = False, True
                        easy_button = Button(menu_green, 0, 0, 0, 0, "Easy")
                        medium_button = Button(menu_green, 0, 0, 0, 0, "Medium")
                        hard_button = Button(menu_green, 0, 0, 0, 0, "Hard")
                        screen.fill(corn_silk)
                        board_hard.draw()
                        cur_board = board_hard
                        game_on = True

                    elif restart_button.click(position):
                        double_break = True
                        break

                    elif reset_button.click(position):
                        cur_board.reset_to_original()

                    elif quit_button.click(position):
                        pygame.quit()

                if event.type == pygame.MOUSEMOTION:
                    if easy_button.click(position):
                        easy_button.color = darker_green
                    elif medium_button.click(position):
                        medium_button.color = darker_green
                    elif hard_button.click(position):
                        hard_button.color = darker_green
                    else:
                        easy_button.color, medium_button.color, hard_button.color = menu_green, menu_green, menu_green

                    if reset_button.click(position):
                        reset_button.color = darker_green
                    elif restart_button.click(position):
                        restart_button.color = darker_green
                    elif quit_button.click(position):
                        quit_button.color = darker_green
                    else:
                        reset_button.color, restart_button.color, quit_button.color = menu_green, menu_green, menu_green

            pygame.display.update()
