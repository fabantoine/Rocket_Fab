import pygame
import pymunk
from pymunk.vec2d import Vec2d
class Ball:
    def __init__(self, space, position, radius=50):
        self.space = space

        # Création du corps de la balle
        mass = 5
        moment = pymunk.moment_for_circle(mass, 0, radius)
        self.body = pymunk.Body(mass, moment)
        self.body.position = position

        # Création de la forme circulaire
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.elasticity = 0.5  # Rebondissement important
        self.shape.friction = 0.3  # Friction moyenne pour rouler
        self.shape.collision_type = 3  # Type de collision unique pour la balle

        # Ajout à l'espace physique
        self.space.add(self.body, self.shape)

        # Configuration du gestionnaire de collision
        # Collision avec les roues (type 2)
        self.space.add_collision_handler(2, 3).begin = self.ball_wheel_collision
        # Si vous avez besoin de collision avec le châssis (type 1)
        self.space.add_collision_handler(1, 3).begin = self.ball_chassis_collision

    @staticmethod
    def ball_wheel_collision(arbiter, space, data):
        """Gestion de la collision entre la balle et les roues"""
        return True  # Permet la collision physique

    @staticmethod
    def ball_chassis_collision(arbiter, space, data):
        """Gestion de la collision entre la balle et le châssis"""
        return True  # Permet la collision physique

    def apply_force(self, force):
        """Applique une force à la balle"""
        self.body.apply_force_at_local_point(force, (0, 0))

    def apply_impulse(self, impulse):
        """Applique une impulsion à la balle"""
        self.body.apply_impulse_at_local_point(impulse, (0, 0))

    def draw(self, screen):
        """Dessine la balle sur l'écran"""
        position = self.body.position
        pygame.draw.circle(
            screen,
            (255, 165, 0),  # Couleur orange
            (int(position.x), int(position.y)),
            int(self.shape.radius)
        )

        # Optionnel : dessiner une ligne pour voir la rotation de la balle
        pygame.draw.line(
            screen,
            (255, 0, 0),  # Ligne rouge
            (position.x, position.y),
            (position.x + self.shape.radius * math.cos(self.body.angle),
             position.y + self.shape.radius * math.sin(self.body.angle))
        )