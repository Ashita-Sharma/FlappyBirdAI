import os
import time
import pygame
import random

time.sleep(0.01)
pygame.font.init()
WIN_WIDTH = 576
WIN_HEIGHT = 800
END_FONT = pygame.font.SysFont("Consolas", 15)
DRAW_LINES = False
BIRD_IMG = [pygame.transform.scale2x(pygame.image.load(os.path.join("", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join(
    "", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("", "bg.png")))
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

    def collide(self, bird):
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

def draw_window(win, bird, pipes, base, score):
    win.blit(BG_IMG, (0, 0))
    pygame.display.set_caption("Flappy Bird")

    for pipe in pipes:
        pipe.draw(win)

    # Score
    text = STAT_FONT.render(f"Score: {score}", 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 150, 10))

    # Draw base and bird
    base.draw(win)
    bird.draw(win)

    pygame.display.update()


def main():
    # Game initialization function
    def reset_game():
        """Reset all game variables"""
        bird = Bird(230, 350)
        base = Base(700)
        pipes = [Pipe(700)]
        score = 0
        return bird, base, pipes, score

    # Initial setup
    bird, base, pipes, score = reset_game()

    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    run = True
    game_over = False  # Track Game Over State

    while run:
        clock.tick(30)

        # Quit Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                # Jump (only if game is running)
                if event.key == pygame.K_SPACE and not game_over:
                    bird.jump()

                # RESTART with R key
                if event.key == pygame.K_r:
                    bird, base, pipes, score = reset_game()
                    game_over = False

        # Only update game if not game over
        if not game_over:
            # MOVE THE BIRD
            bird.move()

            # Pipe logic
            add_pipe = False
            rem = []

            for pipe in pipes:
                # Check collision
                if pipe.collide(bird):
                    print(f"Game Over! Final Score: {score}")
                    print("Press R to restart")
                    game_over = True  # Set game over flag
                    break

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

                if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                    rem.append(pipe)

                pipe.move()

            # Add new pipe
            if add_pipe:
                score += 1
                pipes.append(Pipe(700))

            # Remove old pipes
            for r in rem:
                pipes.remove(r)

            # Check ground/ceiling collision
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                print(f"Game Over! Final Score: {score}")
                print("Press R to restart")
                game_over = True

            # Move base
            base.move()

        #draw everything
        draw_window(win, bird, pipes, base, score)

if __name__ == '__main__':
    main()

