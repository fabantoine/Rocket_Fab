import pygame
import pymunk
from pymunk.vec2d import Vec2d


class Car:
    def __init__(self, space, position, size=(125, 35)):
        self.space = space

        # Création du corps principal (châssis)
        mass = 1000
        moment = pymunk.moment_for_box(mass, size)
        self.body = pymunk.Body(mass, moment)
        self.body.position = position

        # Création de la forme rectangulaire pour le châssis
        self.shape = pymunk.Poly.create_box(self.body, size)
        self.shape.friction = 0.5
        self.shape.elasticity = 0.01
        self.shape.collision_type = 1

        # Ajout du châssis à l'espace
        self.space.add(self.body, self.shape)

        # Création des roues
        wheel_mass = 30
        wheel_radius = 15
        wheel_moment = pymunk.moment_for_circle(wheel_mass, 0, wheel_radius)

        # Roue avant
        self.front_wheel_body = pymunk.Body(wheel_mass, wheel_moment)
        self.front_wheel_body.position = (position[0] + size[0] / 3, position[1] + size[1] / 2 + wheel_radius)
        self.front_wheel_shape = pymunk.Circle(self.front_wheel_body, wheel_radius)
        self.front_wheel_shape.friction = 0.7
        self.front_wheel_shape.elasticity = 0.1
        self.front_wheel_shape.collision_type = 2

        # Roue arrière
        self.rear_wheel_body = pymunk.Body(wheel_mass, wheel_moment)
        self.rear_wheel_body.position = (position[0] - size[0] / 3, position[1] + size[1] / 2 + wheel_radius)
        self.rear_wheel_shape = pymunk.Circle(self.rear_wheel_body, wheel_radius)
        self.rear_wheel_shape.friction = 0.7
        self.rear_wheel_shape.elasticity = 0.1
        self.rear_wheel_shape.collision_type = 2

        # Ajout des roues à l'espace
        self.space.add(self.front_wheel_body, self.front_wheel_shape)
        self.space.add(self.rear_wheel_body, self.rear_wheel_shape)

        # Création des suspensions (contraintes élastiques)
        stiffness = 500.0  # Raideur du ressort
        damping = 400.0  # Amortissement

        # Suspension avant
        anchor_a = (size[0] / 3, size[1] / 2 - 20)
        anchor_b = (0, 0)
        self.front_spring = pymunk.DampedSpring(
            self.body, self.front_wheel_body,
            anchor_a, anchor_b,
            30.0, stiffness, damping
        )
        # Jointure en rainure avant
        self.front_spring_groove = pymunk.constraints.GrooveJoint(
            self.body, self.front_wheel_body,
            (size[0] / 3, 0), (size[0] / 3, 60), (0, 0)
        )
        # Moteur avant
        self.front_motor = pymunk.constraints.SimpleMotor(self.body, self.front_wheel_body, 0)
        self.front_motor.max_force = 10000.0

        # Suspension arrière
        anchor_a = (-size[0] / 3, size[1] / 2 - 20)
        self.rear_spring = pymunk.DampedSpring(
            self.body, self.rear_wheel_body,
            anchor_a, anchor_b,
            30.0, stiffness, damping
        )
        # Jointure en rainure ariere
        self.rear_spring_groove = pymunk.constraints.GrooveJoint(
            self.body, self.rear_wheel_body,
            (-size[0] / 3, 0), (-size[0] / 3, 60), (0, 0)
        )
        # Ajout des suspensions à l'espace
        self.space.add(self.front_spring, self.front_spring_groove, self.rear_spring, self.rear_spring_groove)
        self.space.add(self.front_motor)
        # Désactivation des collisions entre les roues et le châssis
        def no_collision(arbiter, space, data):
            return False

        # Handlers de collision
        self.space.add_collision_handler(1, 2).begin = no_collision

    def apply_force(self, force):
        """Applique une force au centre de masse de la voiture"""
        self.body.apply_force_at_local_point(force, (0, 0))

    def apply_impulse(self, impulse):
        """Applique une impulsion au centre de masse de la voiture"""
        self.body.apply_impulse_at_local_point(impulse, (0, 0))

    def jump(self, force=(0, -1000)):
        """Fait sauter la voiture"""
        self.body.apply_impulse_at_local_point(force)

    def accelerate(self, direction=1):
        """Contrôle l'accélération de la voiture
        direction: 1 pour avancer, -1 pour reculer"""
        self.front_motor.rate = -20 * direction

    def brake(self):
        """Applique les freins en arrêtant le moteur"""
        self.front_motor.rate = 0

    def draw(self, screen):
        """Dessine la voiture sur l'écran pygame"""
        # Dessin du châssis
        vertices = [self.body.local_to_world(v) for v in self.shape.get_vertices()]
        pygame.draw.polygon(screen, (255, 0, 0), vertices)

        # Dessin des roues
        front_pos = self.front_wheel_body.position
        rear_pos = self.rear_wheel_body.position
        pygame.draw.circle(screen, (0, 0, 255),
                           (int(front_pos.x), int(front_pos.y)),
                           int(self.front_wheel_shape.radius))
        pygame.draw.circle(screen, (0, 0, 255),
                           (int(rear_pos.x), int(rear_pos.y)),
                           int(self.rear_wheel_shape.radius))