import pygame
import random

class Game:
    def __init__(self):
        pygame.init()
        self.screen_size = (1000,1000)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Game Of Life')
        self.running = True
        self.play = False
        self.sizecell = 5 #size in pixels
        self.FPS = 120

        self.init_tabs()
        self.main()

    # Initialise all the tables and 
    def init_tabs(self):
        self.tab = (int(self.screen_size[0] / self.sizecell),int(self.screen_size[1]/self.sizecell)) #table template for all other tables
        self.tab_1      = [[0]*self.tab[0] for i in range(self.tab[1])] #tab_1 is actual table draw
        self.tab_2      = [[0]*self.tab[0] for i in range(self.tab[1])] #tab_2 is the futur generation
        self.tab_check  = [[0]*self.tab[0] for i in range(self.tab[1])] #tab_check is use to calculate valor of life

    def printTable(self):
        for i in range(self.tab[0]):
            for j in range(self.tab[1]):
                if self.tab_1[i][j] == 1:
                    self.draw(i,j)

    def addCell(self, x, y):
        self.tab_1[x][y] = 1

    def randGenerate(self):
        for i in range(self.tab[0]):
            for j in range(self.tab[1]):
                self.tab_1[i][j] = random.randint(0,1)

    def tampTab(self):
        for i in range(self.tab[0]):
            for j in range(self.tab[1]):
                self.tab_1[i][j] = self.tab_2[i][j]

    def draw(self, x,y):
        pygame.draw.rect(self.screen, (60,60,150),(x*self.sizecell, y*self.sizecell, self.sizecell, self.sizecell))

    def newGeneration(self):
        for i in range(self.tab[0]):
            for j in range(self.tab[1]):
                self.tab_check[i][j] = self.arroundCheck(i,j)
                
                #si 3 voisine = vivante
                if self.tab_check[i][j] == 3:
                    self.tab_2[i][j] = 1
                
                #si <2 voisines = morte
                elif self.tab_check[i][j] <2:
                    self.tab_2[i][j] = 0
                
                #si >3 voisines = morte
                elif(self.tab_check[i][j] >3):
                    self.tab_2[i][j] = 0
                
                #si 2 voisines = bouge pas
                else:
                    self.tab_2[i][j] = self.tab_1[i][j]

    def arroundCheck(self,x,y):
        value = 0
        if x > 0 and y > 0 and self.tab_1[x-1][y-1] == 1 : value = value + 1
        if y > 0 and self.tab_1[x][y-1] == 1: value = value + 1
        if x < self.tab[0]-1 and y > 0 and self.tab_1[x+1][y-1] == 1: value = value + 1
     
        if x > 0 and self.tab_1[x-1][y] == 1 : value = value + 1
        if x < self.tab[0]-1 and self.tab_1[x+1][y] == 1 : value = value + 1
     
        if x > 0 and y < self.tab[1]-1 and self.tab_1[x-1][y+1] == 1 : value = value + 1
        if y < self.tab[1]-1 and self.tab_1[x][y+1] == 1 : value = value + 1
        if x < self.tab[0]-1 and y < self.tab[1]-1 and self.tab_1[x+1][y+1] == 1 : value = value + 1
        
        return value 
    

    def events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_r:
                    self.randGenerate()
                    print("random generation")
                if event.key == pygame.K_SPACE:
                    if self.play == False:
                        self.play = True
                        print("play")
                    elif self.play == True:
                        self.play = False
                        print("pause")
            if event.type == pygame.MOUSEBUTTONDOWN:
                posX = int(pygame.mouse.get_pos()[0]/self.sizecell)
                posY = int(pygame.mouse.get_pos()[1]/self.sizecell)
                print(posX,posY)
                self.addCell(posX,posY)
    
    def loop(self):
        while self.running:
            self.screen.fill((200,200,200))
            self.printTable()
    
            self.events()

            if self.play == True:
                self.newGeneration()
                self.tampTab()

            pygame.display.update()
            self.clock.tick(self.FPS)

    def main(self):
        self.loop()
