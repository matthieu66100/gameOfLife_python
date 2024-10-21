import pygame
import random

class Game:
    def __init__(self):
        pygame.init()
        self.screen_size = (1000, 1000)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption('Jeu de la Vie')
        self.cell_size = 10
        self.grid_dims = (self.screen_size[0] // self.cell_size, self.screen_size[1] // self.cell_size)
        self.grid = [[0] * self.grid_dims[0] for _ in range(self.grid_dims[1])]
        self.running = True
        self.play = False
        self.offset = [0, 0]
        self.mouse_down = False
        self.show_grid = True  #contrôler l'affichage de la grille

    def draw_grid(self):
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                x = (j * self.cell_size) + self.offset[0]
                y = (i * self.cell_size) + self.offset[1]
                if 0 <= x < self.screen_size[0] and 0 <= y < self.screen_size[1]:
                    if cell:
                        pygame.draw.rect(self.screen, (60, 60, 150), (x, y, self.cell_size, self.cell_size))
                    elif self.show_grid:
                        pygame.draw.rect(self.screen, (220, 220, 220), (x, y, self.cell_size, self.cell_size), 1)

    def update_grid(self):
        new_grid = [[0] * self.grid_dims[0] for _ in range(self.grid_dims[1])]
        for i in range(self.grid_dims[1]):
            for j in range(self.grid_dims[0]):
                neighbors = sum(self.grid[x][y] for x in range(max(0, i-1), min(self.grid_dims[1], i+2))
                                              for y in range(max(0, j-1), min(self.grid_dims[0], j+2))
                                              if (x, y) != (i, j))
                new_grid[i][j] = neighbors == 3 or (neighbors == 2 and self.grid[i][j])
        self.grid = new_grid

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.grid = [[random.randint(0, 1) for _ in range(self.grid_dims[0])] for _ in range(self.grid_dims[1])]
                elif event.key == pygame.K_SPACE:
                    self.play = not self.play
                elif event.key == pygame.K_g:  #afficher/cacher la grille
                    self.show_grid = not self.show_grid
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    self.mouse_down = True
                    self.place_cell()
                elif event.button == 4:  # Molette vers le haut
                    self.zoom_in()
                elif event.button == 5:  # Molette vers le bas
                    self.zoom_out()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Relâchement du clic gauche
                    self.mouse_down = False
            elif event.type == pygame.MOUSEMOTION:
                if self.mouse_down:
                    self.place_cell()

    def place_cell(self):
        pos = pygame.mouse.get_pos()
        grid_x = (pos[0] - self.offset[0]) // self.cell_size
        grid_y = (pos[1] - self.offset[1]) // self.cell_size
        if 0 <= grid_x < self.grid_dims[0] and 0 <= grid_y < self.grid_dims[1]:
            self.grid[grid_y][grid_x] = 1

    def zoom_in(self):
        if self.cell_size < 50:  # Limite de zoom
            self.cell_size += 1
            self.adjust_offset()

    def zoom_out(self):
        if self.cell_size > 2:  # Limite de dézoom
            self.cell_size -= 1
            self.adjust_offset()

    def adjust_offset(self):
        center_x = (self.screen_size[0] // 2 - self.offset[0]) // self.cell_size
        center_y = (self.screen_size[1] // 2 - self.offset[1]) // self.cell_size
        self.offset[0] = self.screen_size[0] // 2 - center_x * self.cell_size
        self.offset[1] = self.screen_size[1] // 2 - center_y * self.cell_size

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.screen.fill((200, 200, 200))
            self.draw_grid()
            self.handle_events()
            if self.play:
                self.update_grid()
            pygame.display.update()
            clock.tick(30)
        pygame.quit()
