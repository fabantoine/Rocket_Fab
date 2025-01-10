import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Définir les dimensions de la fenêtre
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jeu Pygame")

# Couleurs
white = (255, 255, 255)
blue = (0, 0, 255)

# Position initiale du cercle
circle_x = screen_width // 2
circle_y = screen_height // 2
circle_radius = 30

# Vitesse de déplacement
speed = 5

# Boucle principale du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Obtenir les touches pressées
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        circle_x -= speed
    if keys[pygame.K_RIGHT]:
        circle_x += speed
    if keys[pygame.K_UP]:
        circle_y -= speed
    if keys[pygame.K_DOWN]:
        circle_y += speed

    # Remplir l'écran avec du blanc
    screen.fill(white)

    # Dessiner le cercle
    pygame.draw.circle(screen, blue, (circle_x, circle_y), circle_radius)

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Limiter la vitesse de la boucle
    pygame.time.Clock().tick(60)
