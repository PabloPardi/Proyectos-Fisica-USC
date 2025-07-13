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
pygame.display.set_caption("Organismos, Depredadores y Recursos")

# Colores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
ICE = (170, 211, 233)
DARK_GREEN = (0, 143, 57)

# Configuración de tiempo
clock = pygame.time.Clock()
FPS = 60

# Rango de edad máxima
MAX_AGE_RANGE = (600, 700)  # Cada organismo tendrá un máximo de vida aleatorio dentro de este rango


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
        self.energy = 100
        self.reproduction_threshold = 120
        self.speed = random.uniform(1.5, 2.5)
        self.exploration_chance = random.uniform(0.3, 0.5)
        self.separation_distance = random.randint(30, 100)
        self.age = 0
        self.max_age = random.randint(*MAX_AGE_RANGE)

    def find_closest_resource(self, resources):
        if not resources:
            return None
        return min(resources, key=lambda res: math.sqrt((self.x - res.x)**2 + (self.y - res.y)**2))

    def avoid_others(self, organisms):
        dx, dy = 0, 0
        for other in organisms:
            if other != self:
                distance = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
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

        self.x = max(0, min(WIDTH, self.x))
        self.y = max(0, min(HEIGHT, self.y))

    def draw(self):
        color_intensity = max(0, 255 - int((self.age / self.max_age) * 255))
        pygame.draw.circle(screen, (0, 0, color_intensity), (int(self.x), int(self.y)), self.radius)

    def is_dead(self):
        return self.energy <= 0 or self.age >= self.max_age

    def reproduce(self):
        if self.energy >= self.reproduction_threshold:
            self.energy /= 2
            return Organism(self.x + random.randint(-20, 20), self.y + random.randint(-20, 20))
        return None


class Predator:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 12
        self.energy = 120
        self.reproduction_threshold = 160
        self.speed = random.uniform(2.0, 3.0)
        self.age = 0
        self.max_age = random.randint(*MAX_AGE_RANGE)
        self.perception_range = 60  # Rango de percepción limitado
        self.separation_distance = 50  # Distancia mínima entre depredadores

    def find_closest_prey(self, organisms):
        if not organisms:
            return None
        organisms_in_range = [o for o in organisms if math.sqrt((self.x - o.x)**2 + (self.y - o.y)**2) <= self.perception_range]
        if not organisms_in_range:
            return None
        return min(organisms_in_range, key=lambda org: math.sqrt((self.x - org.x)**2 + (self.y - org.y)**2))

    def avoid_others(self, predators):
        dx, dy = 0, 0
        for other in predators:
            if other != self:
                distance = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
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

        self.x = max(0, min(WIDTH, self.x))
        self.y = max(0, min(HEIGHT, self.y))

    def draw(self):
        color_intensity = max(0, 255 - int((self.age / self.max_age) * 255))
        pygame.draw.circle(screen, (color_intensity, 0, 0), (int(self.x), int(self.y)), self.radius)

    def is_dead(self):
        return self.energy <= 0 or self.age >= self.max_age

    def reproduce(self):
        if self.energy >= self.reproduction_threshold:
            self.energy /= 2
            return Predator(self.x + random.randint(-20, 20), self.y + random.randint(-20, 20))
        return None

def check_collision(entity1, entity2):
    distance = math.sqrt((entity1.x - entity2.x)**2 + (entity1.y - entity2.y)**2)
    return distance < entity1.radius + entity2.radius

meteorite_events = []

# Meteorito
def meteorite_event():
    global organisms, predators, resources
    x, y = WIDTH/2, HEIGHT/2

    # Registrar el frame actual
    meteorite_events.append(len(population_history))    

    # Animación del meteorito
    for radius in range(0, 300, 10):
        screen.fill(RED)  # Limpiar pantalla
        pygame.draw.circle(screen, BLACK, (x, y), radius, 2)
        font = pygame.font.Font(None, 36)
        text = font.render("¡Impacto de meteorito!", True, BLACK)
        screen.blit(text, (WIDTH // 2 - 130, HEIGHT // 2 - 20))
        pygame.display.flip()
        clock.tick(30)

    # Reducir las poblaciones
    organisms = organisms[:len(organisms) // 2]
    predators = predators[:len(predators) // 2]
    resources = resources[:len(resources) // 4]

# Evento de glaciación

glaciation_periods = []

def glaciation_event():
    global glaciation_active, glaciation_timer
    glaciation_active = True
    glaciation_timer = GLACIATION_DURATION

    # Registrar el inicio y el final del período de glaciación
    start_frame = len(population_history)
    end_frame = start_frame + GLACIATION_DURATION
    glaciation_periods.append((start_frame, end_frame))

    apply_glaciation_effect()
    show_glaciation_message()

def apply_glaciation_effect():
    for organism in organisms:
        organism.speed /= (4/3) # Reducción de velocidad al 75%
    for predator in predators:
        predator.speed /= (4/3)

def restore_speeds():
    for organism in organisms:
        organism.speed *= (4/3) # Restauración de velocidad
    for predator in predators:
        predator.speed *= (4/3)

def show_glaciation_message():
    """Muestra un mensaje en la pantalla indicando la glaciación."""
    for _ in range(50):  # Muestra el mensaje durante unos frames
        screen.fill(ICE)  # Limpia la pantalla
        font = pygame.font.Font(None, 72)
        text = font.render("GLACIACIÓN", True, (0, 0, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        clock.tick(30)
        

# Gráfica final
def plot_population_history():
    plt.figure(figsize=(12, 6))
    plt.plot(population_history, label="Organismos", color="blue")
    plt.plot(predator_population_history, label="Depredadores", color="red")

    # Sombrear los períodos de glaciación
    for start, end in glaciation_periods:
        plt.axvspan(start, end, color=(0.67,0.83,0.91), alpha=0.5)

    # Agregar una leyenda única para la glaciación
    if glaciation_periods:
        plt.axvspan(0, 0, color=(0.67,0.83,0.91), alpha=0.5, label="Período de Glaciación")
        
    # Dibujar las líneas de los eventos de meteorito
    meteorite_label_added = False  # Bandera para el label del meteorito
    for frame in meteorite_events:
        if not meteorite_label_added:
            plt.axvline(x=frame, color="black", linestyle="--", label="Meteorito")
            meteorite_label_added = True
        else:
            plt.axvline(x=frame, color="black", linestyle="--")
        
    plt.xlabel("Tiempo " + r"($game~ticks$)")
    plt.ylabel("Población")
    plt.legend(loc="upper right")
    plt.grid(True)
    plt.show()

# Inicialización
organisms = [Organism(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(40)]
predators = [Predator(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(10)]
resources = []
resource_spawn_timer = 0
RESOURCE_SPAWN_RATE = 2 # Intervalo de generación de recursos en frames
RESOURCE_SPAWN_RATE_GLACIATION = 30  # Intervalo más lento durante la glaciación

# Configuración para la glaciación
GLACIATION_DURATION = 400  # Duración de la glaciación en frames
glaciation_active = False
glaciation_timer = 0

# Historial de población
population_history = []
predator_population_history = []

# Bucle principal
running = True

while running:
    # Cambiar el color de fondo según el estado de la glaciación
    if glaciation_active:
        screen.fill(ICE)  # Fondo ICE durante la glaciación
    else:
        screen.fill(DARK_GREEN)  # Fondo normal
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Detectar eventos
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                meteorite_event()  # Meteorito
            if event.key == pygame.K_SPACE:
                glaciation_event()  # Glaciación

    # Regeneración de recursos con ajustes
    resource_spawn_timer += 1
    if glaciation_active:
        if resource_spawn_timer > RESOURCE_SPAWN_RATE_GLACIATION:
            resources.append(Resource(random.randint(0, WIDTH), random.randint(0, HEIGHT)))
            resource_spawn_timer = 0
    else:
        if resource_spawn_timer > RESOURCE_SPAWN_RATE:
            resources.append(Resource(random.randint(0, WIDTH), random.randint(0, HEIGHT)))
            resource_spawn_timer = 0

    # Aplicar efecto de glaciación
    if glaciation_active:
        if glaciation_timer == GLACIATION_DURATION:
            apply_glaciation_effect()  # Reducir velocidades

        # Visualizar glaciación con un tinte azul
        s = pygame.Surface((WIDTH, HEIGHT))
        s.set_alpha(100)
        s.fill(ICE)
        screen.blit(s, (0, 0))

        glaciation_timer -= 1
        if glaciation_timer <= 0:
            glaciation_active = False
            restore_speeds()  # Restaurar velocidades normales

    for resource in resources:
        resource.draw()

    for organism in organisms[:]:
        organism.age += 1
        dx, dy = organism.avoid_others(organisms)
        if abs(dx) > 0 or abs(dy) > 0:
            distance = math.sqrt(dx**2 + dy**2)
            organism.x += organism.speed * dx / distance
            organism.y += organism.speed * dy / distance
            organism.energy -= 0.1

        if random.random() < organism.exploration_chance:
            organism.move_randomly()
        else:
            closest_resource = organism.find_closest_resource(resources)
            if closest_resource:
                organism.move_towards(closest_resource)

        organism.draw()

        for resource in resources[:]:
            if check_collision(organism, resource):
                resources.remove(resource)
                organism.energy += 30

        new_organism = organism.reproduce()
        if new_organism:
            organisms.append(new_organism)

        if organism.is_dead():
            organisms.remove(organism)

    for predator in predators[:]:
        predator.age += 1

        dx, dy = predator.avoid_others(predators)
        if abs(dx) > 0 or abs(dy) > 0:
            distance = math.sqrt(dx**2 + dy**2)
            predator.x += predator.speed * dx / distance
            predator.y += predator.speed * dy / distance
            predator.energy -= 0.1

        closest_prey = predator.find_closest_prey(organisms)
        if closest_prey:
            predator.move_towards(closest_prey)
            if check_collision(predator, closest_prey):
                predator.energy += 40
                organisms.remove(closest_prey)
        else:
            predator.move_randomly()

        predator.draw()

        new_predator = predator.reproduce()
        if new_predator:
            predators.append(new_predator)

        if predator.is_dead():
            predators.remove(predator)

    population_history.append(len(organisms))
    predator_population_history.append(len(predators))

    font = pygame.font.Font(None, 24)
    text = font.render(f"Organismos: {len(organisms)} | Depredadores: {len(predators)} | Recursos: {len(resources)}", True, BLACK)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()

# Mostrar la gráfica con eventos
plot_population_history()
