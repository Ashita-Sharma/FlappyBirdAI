import os
import time
import pygame
import neat
import random
import pickle

time.sleep(0.01)
gen = 0
pygame.font.init()
WIN_WIDTH = 576
WIN_HEIGHT = 800
END_FONT = pygame.font.SysFont("Consolas", 15)
DRAW_LINES = False
BIRD_IMG = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
STAT_FONT = pygame.font.SysFont('Consolas', 30)
class Bird:
    IMGS = BIRD_IMG
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0  # degrees to tilt
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]
    # tick works as a way of keeping time while the game runs
    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y
    def move(self):
        self.tick_count += 1

        # for downward acceleration
        displacement = self.vel*(self.tick_count) + 0.5*(3)*(self.tick_count)**2  # calculate displacement
        #this is basically s=(v.t)+(a.t^2)
        # terminal velocity
        if displacement >= 16:
            displacement = (displacement/abs(displacement)) * 16

        if displacement < 0:
            displacement -= 2

        self.y = self.y + displacement
        if displacement < 0 or self.y < self.height + 50:  # tilt up
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:  # tilt down
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL
    def draw(self, win):
        self.img_count += 1

        # For animation of bird, loop through three images
        if self.img_count <= self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count <= self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count <= self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count <= self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0
        #makes sure nothing is left behind
        #when falling no flapping
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2


        rotated_img = pygame.transform.rotate(self.img, self.tilt)
        # rotates image of the bird
        new_rect = rotated_img.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        # makes sur ethe center of the bird rotated is the actual center since
        # a rotated center will have a different dimension of the circumscribing rectangle
        win.blit(rotated_img, new_rect)
        # draws the rotated image

    def get_mask(self):
        # mask is the nontransparent pixels of the bird sprite
        # it is used for exact collision detection instead of using hitboxes
        return pygame.mask.from_surface(self.img)


class Pipe:
    GAP = 200
    VEL = 10

    def set_height(self):
        # randomizing height of pipes
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.gap = 100
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG
        self.passed = False
        self.set_height()

    def move(self):
        # moving of pipes to the left
        self.x -= self.VEL

    def draw(self, win):
        # draw top
        win.blit(self.PIPE_TOP, (self.x, self.top))
        # draw bottom
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird, win):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        # to check coordinates of bird and pipes
        top_offset = (self.x - bird.x, self.top - round(bird.y))

        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))
        # if they do not overlap, returns None
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)
        # vvv makes sure b/t point are not None
        if b_point or t_point:
            return True

        return False


class Base:
    VEL = 10
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        # moves floor
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        # draws the floor as two images that are attacked to each pother with one end
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def draw_window(win, birds, pipes, base, score, gen):
    if gen == 0:
        gen = 1

    win.blit(BG_IMG, (0, 0))
    pygame.display.set_caption("Flappy Bird")
    for pipe in pipes:
        pipe.draw(win)

    # generations
    score_label = STAT_FONT.render("Gens: " + str(gen - 1), 1, (255, 255, 255))
    win.blit(score_label, (10, 10))

    text = STAT_FONT.render(f"Score:{score}", 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 150 - text.get_height(), 10))

    # alive
    score_label = STAT_FONT.render("Alive: " + str(len(birds)), 1, (255, 255, 255))
    win.blit(score_label, (10, 50))

    base.draw(win)
    for bird in birds:
        bird.draw(win)
    pygame.display.update()


# blit is block image transfer
# it is used for layering images

def main(genomes, config):
    global win, gen
    gen += 1

    nets = []
    ge = []
    birds = []
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)  # addds the network+genome+existence of each bird to a corresponding slot(eg:0,1,2, etc.)
        birds.append(Bird(230, 350))  # initializes bird
        g.fitness = 0  # initialize the fitness
        ge.append(g)
    # bird = Bird(230, 350)
    base = Base(700)
    pipes = [Pipe(700)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    score = 0
    run = True
    while run:
        clock.tick(30)

        add_pipe = False
        for event in pygame.event.get():
            # gets/receives information of everything that has happened otherwise it will become unresponsive
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            run = False
            break
        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1
            output = nets[x].activate(
                (bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))
            if output[0] > 0.5:
                bird.jump()
        rem = []
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird, win):
                    ge[x].fitness -= 1  # make sure those who bash into pipes don't get good scores
                    birds.pop(x)  # rip bird, fly high king
                    nets.pop(x)
                    ge.pop(x)
                if not pipe.passed and pipe.x < bird.x:
                    # if pipe goes past the bird

                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
            # if rightmost edge of pipe is gone(since leftmost topmost coordinate is (0,0))
            # remove the pipe
            pipe.move()


        if add_pipe:
            # score logic
            score += 1
            for g in ge:
                g.fitness += 5  #gives good score
            # creates another pipe to be displayed after current pipe crosses the bird
            pipes.append(Pipe(700))
        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(x)  # rip bird, fly high king
                nets.pop(x)
                ge.pop(x)

        for r in rem:
            pipes.remove(r)
            # deletes the pipe that passed just now
        # bird.move()
        base.move()
        draw_window(win, birds, pipes, base, score, gen)
        # break if score gets large enough
        if score > 20:
            pickle.dump(nets[0], open("best.pickle", "wb"))
            break



def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    # to create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    # p.add_reporter(neat.Checkpointer(5))
    winner = p.run(main, 50)

    print('\nBest genome:\n{!s}'.format(winner))

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
