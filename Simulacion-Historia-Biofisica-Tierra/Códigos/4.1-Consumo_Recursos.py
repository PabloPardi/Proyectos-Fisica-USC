'''
El clock.tick de la simulación ha sido establecido a 1000 para realizar las 
simulaciones. Por defecto viene configurado para ser igual a los FPS.
'''

import pygame
import random
import math
import matplotlib.pyplot as plt

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Organismos y Recursos")

# Colores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
DARK_GREEN = (0, 143, 57)

# Configuración de tiempo
clock = pygame.time.Clock()
FPS = 60

# Rango de edad máxima
MAX_AGE_RANGE = (1200, 1500)  # Cada organismo tendrá un máximo de vida aleatorio dentro de este rango

# Tasa de generación de recursos
resource_generation_rate = 10

class Resource:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 5

    def draw(self):
        pygame.draw.circle(screen, GREEN, (self.x, self.y), self.radius)


class Organism:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 10
        self.energy = 99
        self.reproduction_threshold = 100
        self.speed = random.uniform(1.5, 2.5)
        self.exploration_chance = random.uniform(0.3, 0.4)
        self.separation_distance = random.randint(50, 100)
        self.age = random.randint(0,1000)  # Edad inicial aleatoria
        self.max_age = random.randint(*MAX_AGE_RANGE)  # Máxima edad aleatoria

    def find_closest_resource(self, resources):
        if not resources:
            return None
        return min(resources, key=lambda res: math.sqrt((self.x - res.x)**2 + (self.y - res.y)**2))

    def avoid_others(self, organisms):
        dx, dy = 0, 0
        for other in organisms:
            if other != self:
                distance = math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
                if distance < self.separation_distance:
                    dx += self.x - other.x
                    dy += self.y - other.y
        return dx, dy

    def move_towards(self, target):
        if target:
            dx = target.x - self.x
            dy = target.y - self.y
            distance = math.sqrt(dx**2 + dy**2)
            if distance > 0:
                self.x += self.speed * dx / distance
                self.y += self.speed * dy / distance
                self.energy -= 0.2

    def move_randomly(self):
        self.x += random.randint(-3, 3)
        self.y += random.randint(-3, 3)
        self.energy -= 0.1

        # Limitar posición dentro de la pantalla
        self.x = max(0, min(WIDTH, self.x))
        self.y = max(0, min(HEIGHT, self.y))

    def draw(self):
        # Cambiar el color con la edad (opcional)
        color_intensity = max(0, 255 - int((self.age / self.max_age) * 255))
        pygame.draw.circle(screen, (0, 0, color_intensity), (int(self.x), int(self.y)), self.radius)

    def is_dead(self):
        return self.energy <= 0 or self.age >= self.max_age

    def reproduce(self):
        if self.energy >= self.reproduction_threshold:
            self.energy /= 2
            return Organism(self.x + random.randint(-20, 20), self.y + random.randint(-20, 20))
        return None


# Funciones auxiliares
def check_collision(organism, resource):
    distance = math.sqrt((organism.x - resource.x)**2 + (organism.y - resource.y)**2)
    return distance < organism.radius + resource.radius


# Inicialización
organisms = [Organism(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(30)]
resources = []
resource_spawn_timer = 0

# Historial de población
population_history = []

# Bucle principal
running = True

while running:
    screen.fill(DARK_GREEN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Generar recursos periódicamente
    resource_spawn_timer += 1
    if resource_spawn_timer >= resource_generation_rate:  
        resources.append(Resource(random.randint(0, WIDTH), random.randint(0, HEIGHT)))
        resource_spawn_timer = 0

    # Dibujar y actualizar recursos
    for resource in resources:
        resource.draw()

    # Actualizar y dibujar organismos
    for organism in organisms[:]:
        organism.age += 1  # Incrementar la edad en cada frame

        # Evitar otros organismos
        dx, dy = organism.avoid_others(organisms)
        if abs(dx) > 0 or abs(dy) > 0:
            distance = math.sqrt(dx**2 + dy**2)
            organism.x += organism.speed * dx / distance
            organism.y += organism.speed * dy / distance
            organism.energy -= 0.1

        # Decidir si moverse aleatoriamente o buscar el recurso más cercano
        if random.random() < organism.exploration_chance:
            organism.move_randomly()
        else:
            closest_resource = organism.find_closest_resource(resources)
            if closest_resource:
                organism.move_towards(closest_resource)

        organism.draw()

        # Verificar colisión con recursos
        for resource in resources[:]:
            if check_collision(organism, resource):
                resources.remove(resource)
                organism.energy += 30

        # Reproducirse si tienen suficiente energía
        new_organism = organism.reproduce()
        if new_organism:
            organisms.append(new_organism)

        # Eliminar organismos muertos
        if organism.is_dead():
            organisms.remove(organism)

    # Registrar tamaño de la población
    population_history.append(len(organisms))

    # Mostrar información
    font = pygame.font.Font(None, 24)
    text = font.render(f"Organismos: {len(organisms)} | Recursos: {len(resources)}", True, BLACK)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

# Graficar la evolución de la población
plt.figure(figsize=(10, 6))
plt.plot(population_history, label="Población de organismos", color="blue")
plt.ylim(0,100)
plt.xlim(-500,10000)
plt.xlabel("Tiempo " + r"($game~ticks$)")
plt.ylabel("Número de organismos")
plt.legend()
plt.grid(True)
plt.show()
