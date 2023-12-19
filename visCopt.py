import pygame
import sys
import math
from queue import PriorityQueue

pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Pathfinding Visualization")

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
PURPLE = (128, 0, 128)
DARKBLUE = (0, 0, 139)

black_pixel_coordinates = []


# Node class
class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == DARKBLUE

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK
        black_pixel_coordinates.append((self.row, self.col))

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = DARKBLUE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        self.neighbours = []
        if self.row < self.total_rows - 1:
            self.neighbours.append(grid[self.row + 1][self.col])
            if self.col < self.total_rows - 1:
                self.neighbours.append(grid[self.row + 1][self.col + 1])  # Lower-right diagonal
            if self.col > 0:
                self.neighbours.append(grid[self.row + 1][self.col - 1])  # Lower-left diagonal
        if self.row > 0:
            self.neighbours.append(grid[self.row - 1][self.col])
            if self.col < self.total_rows - 1:
                self.neighbours.append(grid[self.row - 1][self.col + 1])  # Upper-right diagonal
            if self.col > 0:
                self.neighbours.append(grid[self.row - 1][self.col - 1])  # Upper-left diagonal
        if self.col < self.total_rows - 1:
            self.neighbours.append(grid[self.row][self.col + 1])
        if self.col > 0:
            self.neighbours.append(grid[self.row][self.col - 1])

    def print_black_pixel_coordinates():
        print("Coordinates of Black Pixels:")
        for coord in black_pixel_coordinates:
            print(f"({coord[0]}, {coord[1]})")

    def make_barrier(self):
        self.color = BLACK
        black_pixel_coordinates.append((self.row, self.col))

    def __lt__(self, other):
        return False


# Fungsi heuristik
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


# Menampilkan jalur
def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def astar(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbour in current.neighbours:
            if not neighbour.is_barrier():
                temp_g_score = g_score[current] + 1

                if temp_g_score < g_score[neighbour]:
                    came_from[neighbour] = current
                    g_score[neighbour] = temp_g_score
                    f_score[neighbour] = temp_g_score + h(neighbour.get_pos(), end.get_pos())
                    if neighbour not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbour], count, neighbour))
                        open_set_hash.add(neighbour)
                        neighbour.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


# Membuat grid
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid


# Menggambar grid
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


# Menggambar semua elemen
def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


# Menerima input dan menangani interaksi pengguna
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def print_black_pixel_coordinates():
    print("Coordinates of Black Pixels:")
    for coord in black_pixel_coordinates:
        print(f"({coord[0]}, {coord[1]})")


def draw_info(win, width):
    font = pygame.font.Font(None, 30)

    # Info teks di sebelah kanan canvas
    info_text = [
        "Controls:",
        "Left Mouse Button: Place Start, End, or Barriers",
        "Right Mouse Button: Remove Start, End, or Barriers",
        "Spacebar: Run A* Algorithm",
        "C: Clear Grid",
        "P: Print Coordinates",
        "Esc: Quit",
    ]

    info_y = 50
    for line in info_text:
        line_text = font.render(line, True, BLACK)
        win.blit(line_text, (width + 10, info_y))
        info_y += 30


# Fungsi utama
def main(win, width):
    ROWS = 40
    grid = make_grid(ROWS, width)

    
    #NO 8
    for i in range(1, 12):
        grid[i][18].make_barrier()
    for i in range(1, 12):
        grid[i][18].make_barrier()



    #NO1
    for i in range(0, 12):
        grid[i][18].make_barrier()

    for i in range(0, 7):
        grid[i][20].make_barrier()
    
    for i in range(8, 12):
        grid[i][20].make_barrier()

    grid[0][19].make_barrier()

    #No 8
    for i in range(20, 32):
        grid[11][i].make_barrier()

    for i in range(20, 32):
        grid[13][i].make_barrier()

    #NO9
    for i in range(14, 32):
        grid[i][31].make_barrier()

    for i in range(13,32):
        grid[i][33].make_barrier()

    #NO10
    for i in range(20, 32):
        grid[31][i].make_barrier()

    for i in range(23, 32):
        grid[33][i].make_barrier()

    #keputih
    for i in range(33, 40):
        grid[i][31].make_barrier()

    for i in range(32, 40):
        grid[i][33].make_barrier()

    #MERR
    for i in range(33, 39):
        grid[11][i].make_barrier()

    for i in range(33, 39):
        grid[13][i].make_barrier()
    
    #No 5
    for i in range(20, 34):
        grid[6][i].make_barrier()

    for i in range(20, 31):
        grid[8][i].make_barrier()

    for i in range(7, 12):
        grid[i][33].make_barrier()
    
    for i in range(8, 12):
        grid[i][31].make_barrier()

    #no 6
    
    #4 ke bawah
    for i in range(7,18 ):
        grid[31][i].make_barrier()

    for i in range(5,18):
        grid[33][i].make_barrier()

    #its
    for i in range(33,37 ): 
        grid[i][18].make_barrier()
    
    for i in range(18,23 ):
        grid[36][i].make_barrier()

    for i in range(34,37 ):
        grid[i][23].make_barrier()
    
    grid[33][19].make_barrier()
    grid[34][19].make_barrier()
    grid[35][19].make_barrier()

    grid[33][20].make_barrier()
    grid[34][20].make_barrier()
    grid[35][20].make_barrier()

    grid[33][22].make_barrier()
    grid[34][22].make_barrier()
    grid[35][22].make_barrier()
    grid[36][22].make_barrier()



    #No 2
    for i in range(14,32):
        grid[i][18].make_barrier()

    for i in range(14,32):
        grid[i][20].make_barrier()


    #No 3
    
    for i in range(5, 19):
        grid[11][i].make_barrier()

    for i in range(7, 19):
        grid[13][i].make_barrier()

    #No 4
        
    for i in range(11, 33):
        grid[i][5].make_barrier()

    for i in range(13, 31):
        grid[i][7].make_barrier()

    




    start = None
    end = None

    run = True
    started = False

    while run:
        draw(win, grid, ROWS, width)
        draw_info(win, width)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if started:
                continue

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbours(grid)
                    started = True  # Mark the algorithm as started
                    astar(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

                if event.key == pygame.K_p:
                    print_black_pixel_coordinates()

            if pygame.mouse.get_pressed()[0]:  # Left mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                elif spot != end and spot != start:
                    spot.make_barrier()

            if pygame.mouse.get_pressed()[2]:  # Right mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

    pygame.quit()


if __name__ == "__main__":
    main(WIN, WIDTH)
