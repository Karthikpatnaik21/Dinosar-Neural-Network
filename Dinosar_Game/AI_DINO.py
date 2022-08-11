import pygame
from pygame.locals import *
import neat
import os
import random
import pickle

# Initiating Game variables

pygame.init()
clock = pygame.time.Clock()
STAT_FOUNT = pygame.font.SysFont("comicsans", 50)
jump_height = 7.5
pygame.display.set_caption("T-Rex Jump Game with AI")
GEN = 0
Vel = 11


class Sprites:
    # Sprite images location
    __directory = os.getcwd()
    __directory += "\Sprites\Dino"
    BG = pygame.image.load(os.path.join(__directory, "BG.png"))
    Floor1 = pygame.image.load(os.path.join(__directory, "Base1.png"))
    Floor2 = pygame.image.load(os.path.join(__directory, "Base2.png"))
    Stand = pygame.image.load(os.path.join(__directory, "Dino Standing.png"))
    Walk = [pygame.image.load(os.path.join(__directory, "Dino 1.png")),
            pygame.image.load(os.path.join(__directory, "Dino 2.png"))]
    Down = [pygame.image.load(os.path.join(__directory, "Dino D1.png")),
            pygame.image.load(os.path.join(__directory, "Dino D2.png"))]
    Death = pygame.image.load(os.path.join(__directory, "Dino death.png"))
    Fly = [pygame.image.load(os.path.join(__directory, "Bird 1.png")),
           pygame.image.load(os.path.join(__directory, "Bird 2.png"))]
    cactus_1 = pygame.image.load(os.path.join(__directory, "Cactus 1.png"))
    cactus_2 = pygame.image.load(os.path.join(__directory, "Cactus 2.png"))
    cactus_3 = pygame.image.load(os.path.join(__directory, "Cactus 3.png"))
    cactuss_1 = pygame.image.load(os.path.join(__directory, "CactusS 1.png"))
    cactuss_2 = pygame.image.load(os.path.join(__directory, "CactusS 2.png"))
    cactuss_3 = pygame.image.load(os.path.join(__directory, "CactusS 3.png"))
    Game_over = pygame.image.load(os.path.join(__directory, "Game Over.png"))
    retry = pygame.image.load(os.path.join(__directory, "Retry.png"))
    cloud = pygame.image.load(os.path.join(__directory, "Cloud.png"))


class Player(object):
    # Initiating player
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.save = y
        self.jump_count = jump_height
        self.walk_count = 0
        self.jump_end = True
        self.standing = False
        self.walking = True
        self.down = False
        self.img = Sprites.Stand

    # defining Jump
    def jump(self):
        if self.jump_count >= -jump_height:
            self.down = False
            self.standing = True
            self.walking = False
            neg = 1
            if self.jump_count < 0:
                neg = -1
            self.y -= round(self.jump_count ** 2 * neg)
            self.jump_count -= 1
            self.img = Sprites.Stand
        else:
            self.standing = False
            self.walking = True
            self.jump_count = jump_height
            self.jump_end = True
            if not self.y == self.save:
                self.y = self.save

    # Defining Lowering head
    def head_down(self):
        if self.jump_end:
            self.walking = False
            self.standing = False
            self.down = True

    # Initiating Movement
    def move(self):
        self.walking = True
        self.standing = False
        self.down = False

    # Drawing player
    def draw(self, windown):
        if not self.down:
            if self.standing:
                windown.blit(Sprites.Stand, (self.x, self.y))
                self.img = Sprites.Stand
            elif self.walking:
                self.walk_count += 1
                if self.walk_count == 2:
                    self.walk_count = 0
                windown.blit(Sprites.Walk[self.walk_count], (self.x, self.y))
                self.img = Sprites.Walk[self.walk_count]
        else:
            self.walk_count += 1
            if self.walk_count == 2:
                self.walk_count = 0
            windown.blit(Sprites.Down[self.walk_count], (self.x, self.y))
            self.img = Sprites.Down[self.walk_count]
        pygame.display.update()

    # Selection of player
    def get_mask(self):
        return pygame.mask.from_surface(self.img.convert_alpha())


class Cactus(object):
    # Initiating Objects
    def __init__(self, number, big, vel):
        self.x = 800
        self.y = 306
        self.posy2 = 0
        self.posy3 = 0
        self.img = Sprites.cactus_1
        self.mask = self.get_mask()
        self.vel = vel
        self.bye = False
        self.number = number
        self.big = big
        if big:
            self.y = 306
        else:
            self.y = 321

    # Making them move
    def move(self):
        self.x -= self.vel
        pygame.display.update()

    # Updating their movement
    def update(self):
        self.posy2 = self.y + self.img.get_width()
        self.posy3 = self.y + self.img.get_height()

    # Drawing them on the screen
    def draw(self, windown):
        if self.big:
            if self.number == 1:
                self.img = Sprites.cactus_1
                self.mask = self.get_mask()
                windown.blit(Sprites.cactus_1, (self.x, self.y))
                self.update()
            if self.number == 2:
                self.img = Sprites.cactus_2
                self.mask = self.get_mask()
                windown.blit(Sprites.cactus_2, (self.x, self.y))
                self.update()
            if self.number == 3:
                self.img = Sprites.cactus_3
                self.mask = self.get_mask()
                windown.blit(Sprites.cactus_3, (self.x, self.y))
                self.update()
        else:
            if self.number == 1:
                self.img = Sprites.cactuss_1
                self.mask = self.get_mask()
                windown.blit(Sprites.cactuss_1, (self.x, self.y))
                self.update()
            if self.number == 2:
                self.img = Sprites.cactuss_2
                self.mask = self.get_mask()
                windown.blit(Sprites.cactuss_2, (self.x, self.y))
                self.update()
            if self.number == 3:
                self.img = Sprites.cactuss_3
                self.mask = self.get_mask()
                windown.blit(Sprites.cactuss_3, (self.x, self.y))
                self.update()

    # Selecting the Objects
    def get_mask(self):
        return pygame.mask.from_surface(self.img.convert_alpha())

    # checking if they hit the player
    def check(self, dinos):
        dino = dinos.get_mask()
        thing = self.mask
        frount = (self.x - dinos.x, self.y - dinos.y)
        hit1 = dino.overlap(thing, frount)
        if hit1:
            return True
        return False


class Bird(object):
    # Creating flying obstacles
    def __init__(self, y, vel):
        self.x = 800
        self.y = 142
        self.vel = vel
        self.height = 46
        self.width = 36
        self.posy2 = 0
        self.posy3 = 0
        self.place = y
        self.bye = False
        self.img = Sprites.Fly[0]
        self.fly = 0
        self.walk_count = 0
        if y == 0:
            self.y = 142
        if y == 1:
            self.y = 288
        if y == 2:
            self.y = 318
        self.update()

    # Moving the birds
    def move(self):
        self.x -= self.vel
        pygame.display.update()

    # Updating the movement of birds
    def update(self):
        self.posy2 = self.y + self.width
        self.posy3 = self.y + self.height

    # Animating the wings
    def wing(self):
        if self.walk_count == 8:
            self.walk_count = 0
        if self.walk_count <= 3:
            self.fly = 1
        if self.walk_count >= 4:
            self.fly = 0

    # Drawing the bird
    def draw(self, windown):
        self.walk_count += 1
        self.wing()
        windown.blit(Sprites.Fly[self.fly], (self.x, self.y))
        self.img = Sprites.Fly[self.fly]

    # Selecting the bird
    def get_mask(self):
        return pygame.mask.from_surface(self.img.convert_alpha())

    # Checking if player hit the object
    def check(self, dinos):
        dino = dinos.get_mask()
        thing = self.get_mask()
        top = (self.x - dinos.x, self.y - dinos.y)
        hit1 = dino.overlap(thing, top)
        if hit1:
            return True
        return False


class Base:
    # Creating the floor and background
    IMG1 = Sprites.Floor1
    IMG2 = Sprites.Floor2
    IMG3 = Sprites.Floor2
    WIDTH = IMG1.get_width()
    WIDTH2 = WIDTH + IMG2.get_width()

    # Creating the base
    def __init__(self, y, vel):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
        self.x3 = self.WIDTH2
        self.vel = vel

    # Making an infinite loop
    def reconfigure_loc(self):
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH2
            return self.x1
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x3 + self.WIDTH2
            return self.x2
        if self.x3 + self.WIDTH < 0:
            self.x3 = self.x1 + self.WIDTH2
            return self.x3

    # Moving the Base to make an illusion of walking
    def move(self, vel):
        self.vel = vel
        self.x1 -= self.vel
        self.x2 -= self.vel
        self.x3 -= self.vel
        pygame.display.update()
        self.reconfigure_loc()

    # Drawing the base
    def draw(self, win):
        win.blit(self.IMG1, (self.x1, self.y))
        win.blit(self.IMG2, (self.x2, self.y))
        win.blit(self.IMG2, (self.x3, self.y))


class cloud:

    # Making clouds
    def __init__(self, vel, y):
        self.x = 800
        self.y = y
        self.vel = vel

    # Moving the clouds
    def move(self):
        self.x -= self.vel

    # Drawing the clouds
    def draw_cloud(self, window):
        window.blit(Sprites.cloud, (self.x, self.y))


def drawgame(score, floor, clouds, obstacle, dinos, window, gen):
    # Drawing the whole game

    # Drawing floor
    window.blit(Sprites.BG, (0, 0))
    floor.draw(window)

    # Drawing Score population etc
    popul = len(dinos)
    text = STAT_FOUNT.render("Population: " + str(popul), True, (255, 255, 255))
    window.blit(text, (10, 45))
    text = STAT_FOUNT.render("Score: " + str(score), True, (255, 255, 255))
    window.blit(text, (790 - text.get_width(), 10))
    text = STAT_FOUNT.render("Gen: " + str(gen), True, (255, 255, 255))
    window.blit(text, (10, 10))

    # Drawing clouds and obstacles
    for summon in clouds:
        summon.draw_cloud(window)
    for obstacles in obstacle:
        obstacles.draw(window)

    # Drawing all the players
    for Dino in dinos:
        Dino.draw(window)

    # Updating the game
    pygame.display.update()


def events(gap, vel):
    # Adding game time and time events
    time = int((gap / vel) * 100)
    pygame.time.set_timer(USEREVENT + 4, 600)
    pygame.time.set_timer(USEREVENT + 3, random.randrange(200, 700))
    pygame.time.set_timer(USEREVENT + 2, random.randrange(time, time + 10))
    pygame.time.set_timer(USEREVENT + 1, 60000)


def main(genomes, config):
    gap = 180
    vel = 11
    Cloud = []
    floor = Base(348, vel)
    Obstacles = []
    Dinos = []
    events(gap, vel)
    nets = []
    ge = []
    global GEN
    GEN += 1
    # Creating the players
    for ids, gens in genomes:
        net = neat.nn.FeedForwardNetwork.create(gens, config)
        nets.append(net)
        Dinos.append(Player(45, 310))
        gens.fitness = 0
        ge.append(gens)
    window = pygame.display.set_mode((800, 420))
    score = 0
    clocks = pygame.time.Clock()

    Start = True
    # Starting the game
    while Start and len(Dinos) > 0:
        clocks.tick(30)
        T = 0
        M = 1
        D = 2
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Start = False
                quit()

            # Randomly spawning the Obstacles
            if event.type == USEREVENT + 2:
                r = random.randrange(0, 9)
                if r == 0:
                    Obstacles.append(Cactus(1, True, vel))
                elif r == 1:
                    Obstacles.append(Cactus(2, True, vel))
                elif r == 2:
                    Obstacles.append(Cactus(3, True, vel))
                elif r == 3:
                    Obstacles.append(Cactus(1, False, vel))
                elif r == 4:
                    Obstacles.append(Cactus(2, False, vel))
                elif r == 5:
                    Obstacles.append(Cactus(3, False, vel))
                elif r == 6:
                    Obstacles.append(Bird(T, vel))
                elif r == 7:
                    Obstacles.append(Bird(M, vel))
                elif r == 8:
                    Obstacles.append(Bird(D, vel))

            # Spawns an obstacle
            if event.type == USEREVENT + 1:
                vel += 1
                gap += 1
                events(gap, vel)

            # Spawns a Cloud
            if event.type == USEREVENT + 3:
                rand = random.randrange(0, 8)
                if rand == 4:
                    Cloud.append(cloud(10, (random.randrange(98, 250))))

            if event.type == USEREVENT + 4:
                score += 1

        obstacle_id = 0
        if len(Obstacles) > 0:
            if len(Dinos) > 0:
                if len(Obstacles) > 1 and Dinos[0].x > Obstacles[0].x:
                    obstacle_id = 1

            # Applying input to Neural network
            for _, Dino in enumerate(Dinos):
                Dino.move()
                ge[_].fitness += 1
                output = nets[Dinos.index(Dino)].activate((Dino.y, abs(Dino.y - Obstacles[obstacle_id].y),
                                                           abs(Dino.x - Obstacles[obstacle_id].x),
                                                           abs(Dino.y - Obstacles[obstacle_id].posy2),
                                                           abs(Dino.y - Obstacles[obstacle_id].posy3)))

                # Getting input from neural network and taking action according to that
                if output[0] > 0.8:
                    if Dino.jump_end:
                        ge[Dinos.index(Dino)].fitness -= 3
                        Dino.standing = True
                        Dino.walking = False
                        Dino.jump_end = False
                        Dino.down = False
                elif output[1] < 0.8:
                    if Dino.jump_end:
                        ge[Dinos.index(Dino)].fitness -= 3
                        Dino.head_down()
                else:
                    ge[Dinos.index(Dino)].fitness += 0.5

        for ids, Dino in enumerate(Dinos):

            if not Dino.jump_end:
                Dino.standing = False
                Dino.walking = True
                Dino.down = False
                Dino.jump()

        for obstacles in Obstacles:
            obstacles.vel = vel
            obstacles.move()
            for Dino in Dinos:

                if obstacles.check(Dino):
                    # If a player hit the obstacle removing them and decreasing the fitness
                    ge[Dinos.index(Dino)].fitness -= 5
                    nets.pop(Dinos.index(Dino))
                    ge.pop(Dinos.index(Dino))
                    Dinos.pop(Dinos.index(Dino))
                    break

                elif (obstacles.x + obstacles.img.get_width()) < Dino.x:
                    # If player passed an obstacle increasing their fitness
                    ge[Dinos.index(Dino)].fitness += 5

        # Moving the obstacles, floor, background

        floor.move(vel)
        for c in Cloud:
            c.move()
        for e in Obstacles:
            if e.x <= -100:
                Obstacles.remove(e)

        # Drawing and updating games
        drawgame(score, floor, Cloud, Obstacles, Dinos, window, GEN)
        pygame.display.update()


# To run default using new neural network
def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)

    # adding population according to configuration
    p = neat.Population(config)  # You can type (config,"\\initial network\\")

    # Print out statistics in the console
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    p.run(main, 500)  # Put winner = p.run(main, 500) to save the data

    # To save the neural network data

    """
    Save_dat = open("Brain1.txt", "wb")
    pickle.dump(winner, Save_dat)
    Save_dat.close()
    """


# To load a saved neural network data and rum
def replay_genome(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)

    # Opening the previous neural network data
    with open("300 no-Hit.txt", "rb") as brain:
        genome = pickle.load(brain)
    genomes = [(1, genome)]
    main(genomes, config)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    # open Configuration path
    config_patn = os.path.join(local_dir, "NEAT.txt")
    run(config_patn)
