import pygame
import pymunk

# Initialisation de Pygame
pygame.init()

# Configuration de la fenêtre de jeu
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("2D Rocket League")

# Configuration de Pymunk
space = pymunk.Space()
space.gravity = (0, 1)

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
        space.add(line)

create_walls(space, 800, 600)

def create_car(space, position):
    body = pymunk.Body(1, pymunk.moment_for_box(1, (50, 30)))
    body.position = position
    shape = pymunk.Poly.create_box(body, (50, 30))
    shape.elasticity = 0.2
    space.add(body, shape)
    return body

def create_ball(space, position):
    body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 30))
    body.position = position
    shape = pymunk.Circle(body, 30)
    shape.elasticity = 0.6
    space.add(body, shape)
    return body

car1 = create_car(space, (300, 300))
#car2 = create_car(space, (600, 300))
ball = create_ball(space, (400, 300))


def handle_input(car):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        car.apply_force_at_local_point((-5, 0), (0, 0))
    if keys[pygame.K_RIGHT]:
        car.apply_force_at_local_point((5, 0), (0, 0))
    if keys[pygame.K_UP]:
        car.apply_force_at_local_point((0, -2), (0, 0))
    if keys[pygame.K_DOWN]:
        car.apply_force_at_local_point((0, 2), (0, 0))

def draw_objects(screen, space):
    for shape in space.shapes:
        if isinstance(shape, pymunk.Poly):
            points = shape.get_vertices()
            points = [(int(p.x+shape.body.position.x), int(p.y+shape.body.position.y)) for p in points]
            pygame.draw.polygon(screen, (255, 0, 0), points)
        elif isinstance(shape, pymunk.Circle):
            pygame.draw.circle(screen, (0, 255, 0), (int(shape.body.position.x), int(shape.body.position.y)), int(shape.radius))

# Boucle principale du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    handle_input(car1)
    #handle_input(car2)

    space.step(1/60.0)
    screen.fill((0, 0, 0))
    draw_objects(screen, space)
    pygame.display.flip()

pygame.quit()


