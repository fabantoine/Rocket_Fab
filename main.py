'''A VOIR https://github.com/Filbert-code/Python-Pymunk-Vehicle-Simulator/blob/main/Simluator/Sportscar.py


'''
import pygame
import pymunk
from pymunk.pygame_util import DrawOptions
from car import Car
from car2 import Car2

# Initialisation de Pygame
pygame.init()

# Configuration de la fenêtre de jeu
screen = pygame.display.set_mode((960, 540))
pygame.display.set_caption("2D Rocket League")

# Configuration de Pymunk
space = pymunk.Space()
space.gravity = (0, 2)
draw_options = pymunk.pygame_util.DrawOptions(screen)
# Création du terrain de jeu
def create_walls(space, width, height):
    static_lines = [
        pymunk.Segment(space.static_body, (0, 0), (width, 0), 1),
        pymunk.Segment(space.static_body, (0, 0), (0, height), 1),
        pymunk.Segment(space.static_body, (0, height), (width, height), 1),
        pymunk.Segment(space.static_body, (width, 0), (width, height), 1)
    ]
    for line in static_lines:
        line.elasticity = 1.0
        line.friction = 1.0
        space.add(line)

create_walls(space, screen.get_width(), screen.get_height())


def handle_input(car):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        car.accelerate(1)  # Avancer vers la droite
    elif keys[pygame.K_LEFT]:
        car.accelerate(-1)  # Avancer vers la gauche
    elif keys[pygame.K_UP]:
        car.jump((0, -100))  # Avancer vers la gauche
    else:
        car.brake()  # Freiner

# Création de la voiture
car = Car(space, (200, 300))

# Boucle principale du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    space.step(1/60.0)
    screen.fill((0, 0, 0))
    space.debug_draw(draw_options)
    handle_input(car)
    #car.draw(screen)
    pygame.display.flip()

pygame.quit()


