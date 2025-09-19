import os
import time
import pygame
import neat
import random
WIN_WIDTH = 600
WIN_HEIGHT = 800

BIRD_IMG = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

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
    VEL = 5

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

        def set_height(self):
            # randomizing height of pipes
            self.height = random.randrange(50, 450)
            self.top = self.height - self.PIPE_TOP.get_height()
            self.bottom = self.height + self.GAP

        def move(self):
            # moving of pipes to the left
            self.x -= self.VEL

        def draw(self, win):
            # draw top
            win.blit(self.PIPE_TOP, (self.x, self.top))
            # draw bottom
            win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))


def draw_window(win, bird):
    win.blit(BG_IMG, (0, 0))
    bird.draw(win)
    pygame.display.update()


# blit is block image transfer
# it is used for layering images

def main():
    bird = Bird(0, 0)
    run = True
    while run:
        for event in pygame.event.get():
            #gets/receives information of everything that has happened otherwise it will become unresponsive
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()
    quit()

main()
while True:
    pass


