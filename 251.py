import pygame
import neat
import time
import os
import random

import pygame.mask
pygame.font.init()
WIN_WIDTH = 500
WIN_HEIGHT = 800

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))

STAT_FONT = pygame.font.SysFont("comicsans",50)
class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self,x,y):
        """
    self.x: The x-coordinate of the bird's position.
    self.y: The y-coordinate of the bird's position.
    self.tilt: The tilt angle of the bird's image (used for animation).
    self.tick_count: A counter to keep track of time for animation purposes.
    self.vel: The velocity (speed) at which the bird is moving.
    self.height: The initial height of the bird.
    self.img_count: A counter to keep track of the current image for animation.
    self.img: The current image of the bird (initialized with the first image in BIRD_IMGS list).

        """
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        """
        self.vel = -10.5: This line sets the velocity (vel) of the bird to -10.5. By setting a negative value, it causes the bird to move upward (opposite to gravity) and initiates the jump.
        self.tick_count = 0: This line resets the tick_count to 0. The tick_count is used for timing purposes, and by setting it to 0, it ensures that the bird's animation starts fresh.
        self.height = self.y: This line updates the height attribute of the bird to its current y position. It is used to calculate the tilt angle during animation.

        In summary, when the jump method is called, the bird's velocity is set to a negative value to make it move upward, the tick_count is reset to 0, and the height is updated.
        These changes will result in the bird appearing to jump and start the animation sequence.
        :return:
        """
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        """
        The move method is responsible for updating the position and tilt of the bird during each frame of the game. It takes into account gravity and the bird's velocity to simulate realistic movement. Here's what each line of the method does:
self.tick_count += 1: This line increments the tick_count by 1. The tick_count is used for timing purposes and keeps track of how many frames have passed since the last jump.
d = self.vel*self.tick_count + 1.5*self.tick_count**2: This line calculates the displacement (d) of the bird based on its velocity (vel) and the number of frames passed (tick_count). It uses a formula that simulates the effect of gravity and acceleration.
if d >= 16: d = 16: This line limits the maximum downward velocity of the bird to 16. If the calculated displacement exceeds 16, it is capped at 16 to prevent the bird from falling too fast.
if d < 0: d -= 2: This line applies a small upward adjustment to the displacement if the bird is moving upward. This helps to create a smoother jump motion.
self.y = self.y + d: This line updates the y position of the bird by adding the calculated displacement d. It moves the bird up or down based on the current velocity and acceleration.
if d < 0 or self.y < self.height + 50: ...: This block of code handles the tilting of the bird during upward and downward movement. If the bird is moving upward or its current position is close to its initial height plus an offset of 50 pixels, it tilts up. The tilt attribute is gradually adjusted to simulate the bird's rotation.
else: if self.tilt > -90: self.tilt -= self.ROT_VEL: This block of code handles the tilting of the bird during downward movement. If the bird is not moving upward and its tilt is greater than -90 (not fully tilted downward), it gradually tilts downward by subtracting ROT_VEL from the tilt attribute.
In summary, the move method updates the position and tilt of the bird based on its velocity and acceleration. It calculates the displacement, limits the downward velocity, adjusts the displacement for smooth motion, updates the position, and handles the tilting of the bird based on its movement direction. This method is typically called once per frame to animate the bird's movement in the game.

        """
        self.tick_count += 1
        # for downward acceleration
        d = self.vel*self.tick_count + 1.5*self.tick_count**2
            # -10.5 + 1.5 = -9 (tick_count = 1)
        if d >= 16: # moving down like up
            d  = 16
        if d < 0:
            d -=2 # moving upward like down
        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:  # tilt up
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
                if self.tilt > -90:
                    self.tilt -=self.ROT_VEL

    def draw(self,win):
        """
The draw method is responsible for rendering the bird on the game window. It handles the animation and rotation of the bird's image. Here's what each line of the method does:

self.img_count += 1: This line increments the img_count attribute by 1, which keeps track of the number of frames that have passed since the last animation change.
The following block of code determines which image to display based on the current img_count value and the ANIMATION_TIME constant:
If img_count is less than ANIMATION_TIME, it sets the bird's image to IMGS[0] (the first bird image).
If img_count is between ANIMATION_TIME and ANIMATION_TIME*2, it sets the bird's image to IMGS[1] (the second bird image).
If img_count is between ANIMATION_TIME*2 and ANIMATION_TIME*3, it sets the bird's image to IMGS[2] (the third bird image).
If img_count is between ANIMATION_TIME*3 and ANIMATION_TIME*4, it sets the bird's image back to IMGS[1].
If img_count is between ANIMATION_TIME*4 and ANIMATION_TIME*4 + 1, it sets the bird's image back to IMGS[0]. It also resets img_count to 0, starting the animation cycle again.
The next block of code handles the special case when the bird is fully tilted downward (tilt <= -80 degrees). In this case, it sets the bird's image to IMGS[1] (the second bird image) and sets img_count to ANIMATION_TIME*2, effectively freezing the animation at the downward tilt position.
The following lines of code rotate the bird's image (self.img) based on the current tilt (self.tilt) using pygame.transform.rotate(). It creates a new rotated image and calculates its rectangle.
Finally, the rotated image is blitted (rendered) onto the game window (win) at the appropriate position (new_rect.topleft), ensuring that the bird appears rotated and animated correctly.
In summary, the draw method handles the animation and rotation of the bird's image based on the img_count and tilt attributes. It selects the appropriate image based on the animation cycle and tilt angle, rotates the image, and renders it on the game window. This method is typically called once per frame to update the bird's visual representation in the game.
        """
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0] # first flppy brd
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img  = self.IMGS[1] # second brd
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img  = self.IMGS[2] # third brd
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img  = self.IMGS[1] # first brd
        elif self.img_count < self.ANIMATION_TIME*4 + 1:
            self.img  = self.IMGS[0] # first brd
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        # rotated_image = pygame.transform.rotate(self.img,self.tilt)
        # new_rect = rotated_image.get_rect(center=self.img.get_rect(topLeft = (self.x,self.y)).center)
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x,self.y)).center)
        win.blit(rotated_image,new_rect.topleft)

    def get_mask(self):#  gets the mask for the current image of the bird
        """
The get_mask method in the Bird class is responsible for obtaining the mask for the current image of the bird. Masks are used for pixel-perfect collision detection in games.
pygame.mask.from_surface(self.img): This line creates a mask from the surface of the current bird image (self.img). The from_surface function is a Pygame method that takes a surface as input and generates a mask based on the non-transparent pixels of the surface. The mask represents the shape of the bird's image, which can be used for collision detection with other game objects.
 This keyword indicates that the method should return the generated mask.
In summary, the get_mask method retrieves the mask for the current image of the bird. The mask represents the shape of the bird's image and is useful for collision detection purposes.
        """
        return pygame.mask.from_surface(self.img)

class Pipe():
    """
The Pipe class represents a pipe object in the game. Here's a brief explanation of the class and its methods:
GAP = 200 and VEL = 5: These are class-level constants that define the gap between pipes and the velocity at which the pipes move.
__init__(self, x): This is the constructor method of the Pipe class. It initializes the pipe object with the given x coordinate. The height, gap, top, bottom, PIPE_TOP, PIPE_BOTTOM, and passed attributes are also initialized.
self.set_height(): This method is called within the constructor to set the height of the pipe. It randomly determines the height based on the gap and the screen size.
self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True): This line creates the image of the top pipe by flipping the original pipe image (PIPE_IMG) vertically.
self.PIPE_BOTTOM = PIPE_IMG: This line assigns the original pipe image to the PIPE_BOTTOM attribute, representing the bottom pipe.
self.passed = False: This attribute indicates whether the bird has passed this pipe or not. It is initially set to False.

In summary, the Pipe class represents a pipe object in the game. It holds information such as position, height, images for the top and bottom pipes, and a flag indicating whether the bird has passed the pipe or not. The set_height method randomly determines the height of the pipe.


    """
    GAP = 200
    VEL = 5

    def __init__(self, x):
        """
In the __init__ method of the Pipe class, the following steps are performed:

self.x = x: Assigns the given x coordinate to the x attribute of the pipe object.
self.height = 0: Initializes the height attribute to 0. This attribute will later be set to a random value using the set_height method.
self.gap = 100: Sets the gap attribute to 100. This represents the vertical gap between the top and bottom pipes.
self.top = 0 and self.bottom = 0: Initializes the top and bottom attributes to 0. These attributes will hold the y-coordinates of the top and bottom pipes.
self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True): Creates the image for the top pipe by flipping the original pipe image (PIPE_IMG) vertically.
self.PIPE_BOTTOM = PIPE_IMG: Assigns the original pipe image to the PIPE_BOTTOM attribute, representing the image for the bottom pipe.
self.passed = False: Initializes the passed attribute to False. This attribute will later be used to check if the bird has passed this pipe.
self.set_height(): Calls the set_height method to randomly determine the height of the pipe.
Overall, this __init__ method initializes the attributes of the Pipe object, including the position, height, images for the top and bottom pipes, and the flag indicating whether the bird has passed the pipe or not.

        """
        self.x = x
        self.height = 0
        self.gap = 100

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG,False,True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        """
The set_height method of the Pipe class is responsible for setting the height of the pipe object. Here's a brief explanation of what it does:
self.height = random.randrange(50, 450): Generates a random height value between 50 and 450 (exclusive) using the random.randrange function. This height represents the y-coordinate of the gap between the top and bottom pipes.
self.top = self.height - self.PIPE_TOP.get_height(): Calculates the y-coordinate of the top pipe by subtracting the height of the top pipe image (PIPE_TOP) from the generated height. This ensures that the top pipe is positioned correctly above the gap.
self.bottom = self.height + self.GAP: Calculates the y-coordinate of the bottom pipe by adding the generated height to the gap value (GAP). This ensures that the bottom pipe is positioned correctly below the gap.
In summary, the set_height method sets the height and positions of the top and bottom pipes based on a randomly generated height value and the gap value.
        """
        self.height = random.randrange(50,450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        """
The move method of the Pipe class is responsible for moving the pipe object horizontally. Here's a brief explanation of what it does:
self.x -= self.VEL: Subtracts the velocity value (VEL) from the current x-coordinate (self.x) of the pipe. This causes the pipe to move towards the left side of the screen.
In summary, the move method updates the x-coordinate of the pipe by subtracting the velocity, resulting in the pipe moving towards the left side of the screen.
        """
        self.x -= self.VEL

    def draw(self,win):
        """
The draw method of the Pipe class is responsible for drawing the pipe object on the game window. Here's a brief explanation of what it does:
win.blit(self.PIPE_TOP, (self.x, self.top)): Blits (draws) the top part of the pipe (PIPE_TOP) onto the game window (win) at the specified coordinates (self.x, self.top). This positions the top part of the pipe at its current x-coordinate (self.x) and the top y-coordinate (self.top).
win.blit(self.PIPE_BOTTOM, (self.x, self.bottom)): Blits (draws) the bottom part of the pipe (PIPE_BOTTOM) onto the game window (win) at the specified coordinates (self.x, self.bottom). This positions the bottom part of the pipe at its current x-coordinate (self.x) and the bottom y-coordinate (self.bottom).
In summary, the draw method draws both the top and bottom parts of the pipe onto the game window at their respective positions based on the pipe's current x-coordinate (self.x) and the top (self.top) and bottom (self.bottom) y-coordinates.
        """
        win.blit(self.PIPE_TOP,(self.x,self.top))
        win.blit(self.PIPE_BOTTOM,(self.x,self.bottom))

    def collide(self,bird,win):
        """
The collide method of the Pipe class is responsible for checking collision between the bird and the pipe. Here's a brief explanation of what it does:
bird_mask = bird.get_mask(): Retrieves the mask for the current image of the bird using the get_mask method of the bird object.
top_mask = pygame.mask.from_surface(self.PIPE_TOP): Creates a mask from the surface of the top part of the pipe (PIPE_TOP) using the from_surface method of the pygame.mask module.
bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM): Creates a mask from the surface of the bottom part of the pipe (PIPE_BOTTOM) using the from_surface method of the pygame.mask module.
top_offset = (self.x - bird.x, self.top - round(bird.y)): Calculates the offset between the pipe's x-coordinate (self.x) and the bird's x-coordinate (bird.x), and between the pipe's top y-coordinate (self.top) and the rounded bird's y-coordinate (round(bird.y)). This offset is used to determine the relative position of the bird's mask to the top part of the pipe's mask.
bottom_offset = (self.x - bird.x, self.bottom - round(bird.y)): Calculates the offset between the pipe's x-coordinate (self.x) and the bird's x-coordinate (bird.x), and between the pipe's bottom y-coordinate (self.bottom) and the rounded bird's y-coordinate (round(bird.y)). This offset is used to determine the relative position of the bird's mask to the bottom part of the pipe's mask.
b_point = bird_mask.overlap(bottom_mask, bottom_offset): Checks if there is an overlap between the bird's mask and the bottom part of the pipe's mask, using the specified offset. Returns the point of overlap, if any.
t_point = bird_mask.overlap(top_mask, top_offset): Checks if there is an overlap between the bird's mask and the top part of the pipe's mask, using the specified offset. Returns the point of overlap, if any.
if t_point or b_point: return True: Checks if there is a collision between the bird and either the top or bottom part of the pipe. If there is a collision, it returns True.
return False: If there is no collision, it returns False.
In summary, the collide method calculates the masks for the bird and the pipe, determines the relative positions between the masks, and checks for overlap between the bird's mask and the top and bottom parts of the pipe's mask. If there is a collision, it returns True; otherwise, it returns False.
        """
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x,self.top - round(bird.y))
        bottom_offset = (self.x - bird.x , self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask,bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)
        if t_point or b_point:
            return True


        return False


class Base:
    """
This is a class called Base. It represents the base or ground in a game environment. Here's a brief explanation of the class and its attributes:

VEL: This class attribute represents the velocity or speed at which the base moves.
WIDTH: This class attribute stores the width of the base image.
IMG: This class attribute holds the image of the base.
The __init__ method is the constructor of the class. It initializes the object of the Base class with the following attributes:

y: The y-coordinate of the base.
x1: The initial x-coordinate of the base.
x2: The x-coordinate that determines the end position of the base. It is set to the initial x-coordinate plus the width of the base image.
The x1 and x2 values are used to track the movement of the base by updating their values as the base moves horizontally.
    """
    VEl = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self,y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        """

The move method in the Base class is responsible for moving the base image horizontally. Here's a brief explanation of the code:

self.x1 -= self.VEl and self.x2 -= self.VEl: These lines subtract the velocity (VEl) from the x1 and x2 coordinates of the base, causing it to move towards the left.

if self.x1 + self.WIDTH < 0: This condition checks if the left edge of the first base image (x1 + WIDTH) has moved completely off the screen (to the left). If it has, the following line of code is executed:

self.x1 = self.x2 + self.WIDTH: It sets the x1 coordinate to the right of the second base image, ensuring a continuous loop of base images moving from right to left.
if self.x2 + self.WIDTH < 0: This condition checks if the left edge of the second base image (x2 + WIDTH) has moved completely off the screen (to the left). If it has, the following line of code is executed:

self.x2 = self.x1 + self.WIDTH: It sets the x2 coordinate to the right of the first base image, ensuring a continuous loop of base images moving from right to left.
In summary, the move method continuously updates the positions of the base images, creating an illusion of a scrolling background as they move from right to left.
        """
        self.x1 -= self.VEl
        self.x2 -= self.VEl

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self,win):
        """
The draw method in the Base class is used to draw the base images on the game window. Here's a brief explanation of the code:

win.blit(self.IMG, (self.x1, self.y)): This line blits (i.e., draws) the base image (self.IMG) on the game window at the coordinates (self.x1, self.y). This represents the first instance of the base image.

win.blit(self.IMG, (self.x2, self.y)): This line blits the base image (self.IMG) on the game window at the coordinates (self.x2, self.y). This represents the second instance of the base image.

By drawing two base images, one after the other, the illusion of continuous scrolling is created, giving the appearance of a moving base in the game.
        """
        win.blit(self.IMG,(self.x1,self.y))
        win.blit(self.IMG,(self.x2,self.y))



def draw_window(win, birds, pipes, base, score):
    """
The draw_window function is responsible for drawing the game window with all its elements. Here's a brief explanation of the code:

win.blit(BG_IMG, (0, 0)): This line blits (i.e., draws) the background image (BG_IMG) on the game window at coordinates (0, 0). It fills the entire window with the background image.

for pipe in pipes: pipe.draw(win): This loop iterates over each pipe object in the pipes list and calls the draw method of the pipe object, which draws the pipe on the game window.

text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255)): This line creates a text surface with the current score, using the STAT_FONT font. The score is converted to a string and concatenated with the "Score: " label.

win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10)): This line blits the score text on the game window at the specified coordinates. The WIN_WIDTH constant is used to calculate the x-coordinate so that the score appears aligned to the right side of the window.

base.draw(win): This line calls the draw method of the base object, which draws the base images on the game window.

for bird in birds: bird.draw(win): This loop iterates over each bird object in the birds list and calls the draw method of the bird object, which draws the bird on the game window.

pygame.display.update(): This line updates the display to show all the elements that have been blitted on the game window.

Overall, the draw_window function combines the drawing of the background, pipes, score, base, and birds to create the complete game window for each frame of the game.

    """
    win.blit(BG_IMG,(0,0))
    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: " + str(score),1,(255,255,255))
    win.blit(text,(WIN_WIDTH - 10 - text.get_width(),10))

    base.draw(win)

    for bird in birds: # error is occuring chat gpt in this line
        bird.draw(win)

    pygame.display.update()

def main(genomes,config):
    """
The main function is the main loop of the game and is called for each generation of the NEAT algorithm. Here's a brief explanation of the code:
nets = [], ge = [], birds = []: These empty lists will store the neural networks (nets), genomes (ge), and bird objects (birds) for the current generation.
for _, g in genomes:: This loop iterates over the genomes passed to the main function. Each genome consists of an ID and a genetic encoding.
net = neat.nn.FeedForwardNetwork.create(g, config): This line creates a neural network (net) using the genetic encoding (g) and the NEAT configuration (config). This network will be used to control the behavior of a bird.
nets.append(net): The created neural network is added to the nets list.
birds.append(Bird(230, 350)): A new Bird object is created with starting coordinates (230, 350) and added to the birds list.
g.fitness = 0: The fitness of the genome is set to 0 initially. The fitness will be updated based on the performance of the corresponding bird.
ge.append(g): The genome is added to the ge list for tracking purposes.
Overall, the main function initializes the neural networks, bird objects, and genomes for the current generation, setting their initial states and connecting them together.
    """
    nets = []
    ge = []
    birds = []

    for _, g in genomes:
         net = neat.nn.FeedForwardNetwork.create(g,config)
         nets.append(net)
         birds.append(Bird(230,350))
         g.fitness = 0
         ge.append(g)


    """
    This code represents the main game loop for the Flappy Bird game. Here's a brief explanation of the code:

base = Base(730): Creates a Base object representing the ground surface at y-coordinate 730.

pipes = [Pipe(600)]: Creates a list with a single Pipe object placed at x-coordinate 600.

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT)): Creates the game window with the specified width and height.

clock = pygame.time.Clock(): Creates a clock object to control the game's frame rate.

score = 0: Initializes the score to 0.

run = True: The main game loop runs while run is True.

while run:: Starts the main game loop.

clock.tick(30): Limits the frame rate to 30 frames per second.

Event handling: Checks for and handles the quit event to exit the game.

pipe_ind = 0: Initializes the index of the pipe that the birds will consider for making decisions.

Neural network activation: Activates the neural networks for each bird and makes decisions based on their outputs.

Bird movement and fitness update: Moves each bird, increases its fitness, and checks for collision with the pipes.

Pipe management: Updates the positions of the pipes, checks for collision with birds, removes passed pipes, and adds new pipes.

Scoring: Increases the score when a bird passes through a pipe and updates the fitness of all birds.

Bird removal: Removes birds that hit the ground or fly above the screen.

Base movement: Moves the base surface.

Drawing: Calls the draw_window function to update the game window with the current state.

In summary, this main game loop handles events, updates the game state, and draws the updated game window for each frame. It controls the flow of the game and manages the interaction between birds, pipes, and the game environment.
    """
    base = Base(730)
    pipes = [Pipe(600)]
    win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    clock = pygame.time.Clock()

    score = 0
    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
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

        for x,bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1

            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height),abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:
                bird.jump()

        add_pipe = False
        rem = []
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird,win):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if pipe.collide(bird,win):
                    pass



                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5

            pipes.append(Pipe(600))

        for r in rem:
            pipes.remove(r)

        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)



        base.move()
        draw_window(win,birds,pipes,base,score)


"""
This code defines a run function that executes the NEAT algorithm to evolve a population of birds playing the Flappy Bird game. Here's a brief explanation of the code:

run(config_path): The main entry point of the script, it runs the NEAT algorithm using the provided configuration file.

config = neat.config.Config(...): Loads the NEAT configuration from the specified config_path file.

p = neat.Population(config): Creates a new NEAT population based on the provided configuration.

p.add_reporter(neat.StdOutReporter(True)): Adds a reporter that outputs the progress and statistics of the evolution to the console.

stats = neat.StatisticsReporter(): Creates a statistics reporter to track and record various statistics during the evolution.

p.add_reporter(stats): Adds the statistics reporter to the population.

winner = p.run(main, 50): Runs the NEAT algorithm for 50 generations, using the main function as the fitness evaluation function for each generation. The best genome (winner) is returned.

if __name__ == "__main__":: This block ensures that the code is only executed if the script is run directly, not imported as a module.

local_dir = os.path.dirname(__file__): Retrieves the directory path of the current script.

config_path = os.path.join(local_dir, "neat_conf.txt"): Constructs the full path to the NEAT configuration file.

run(config_path): Calls the run function with the configuration path to start the NEAT algorithm.

In summary, this code sets up and runs the NEAT algorithm using a specified configuration file. It manages the evolution of the bird population and outputs the progress and statistics of the evolution. The main function is used as the fitness evaluation function to evaluate each generation of birds.
"""
def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,neat.DefaultStagnation,
                                config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main,50)#we are just calling the main fun to run the bird 50 times

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"neat_conf.txt")
    run(config_path)


