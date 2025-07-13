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
DARK_GREEN = (0, 143, 57)

# Configuración de tiempo
clock = pygame.time.Clock()
FPS = 60

# Rango de edad máxima
MAX_AGE_RANGE = (500, 600)  # Cada organismo tendrá un máximo de vida aleatorio dentro de este rango


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
        self.energy = 119
        self.reproduction_threshold = 160
        self.speed = random.uniform(2.0, 3.0)
        self.age = 0
        self.max_age = random.randint(*MAX_AGE_RANGE)
        self.perception_range = 50  # Rango de percepción limitado
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

# Gráfica final
def plot_population_history():
    plt.figure(figsize=(12, 6))
    plt.plot(population_history, label="Organismos", color="blue")
    plt.plot(predator_population_history, label="Depredadores", color="red") 
    #plt.xlim(0,5000)    
    plt.xlabel("Tiempo " + r"($game~ticks$)")
    plt.ylabel("Población")
    plt.legend(loc="upper right")
    plt.grid(True)
    plt.show()

# Inicialización
organisms = [Organism(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(40)]
predators = [Predator(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(8)]
resources = []
resource_spawn_timer = 0
RESOURCE_SPAWN_RATE = 2  # Intervalo de generación de recursos en frames

# Historial de población
population_history = []
predator_population_history = []
population_history_fit = []
predator_population_history_fit = []

# Listas para registrar tiempos de vida
organism_lifespans = []
predator_lifespans = []

# Bucle principal
running = True
CONT = 0
FRAME_LIMIT_FOR_DATA = 5000  # Limitar el número de frames de muestreo

while running:

    screen.fill(DARK_GREEN) 
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Regeneración de recursos 
    if resource_spawn_timer >= RESOURCE_SPAWN_RATE:
        # Generar un nuevo recurso en una posición aleatoria
        resources.append(Resource(random.randint(0, WIDTH), random.randint(0, HEIGHT)))
        resource_spawn_timer = 0  # Reiniciar el temporizador
    
    # Dibujar todos los recursos en la pantalla
    for resource in resources:
        resource.draw()

    resource_spawn_timer += 1

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
            organism_lifespans.append(organism.age)  # Registrar edad al morir
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
            predator_lifespans.append(predator.age)  # Registrar edad al morir
            predators.remove(predator)

    # Limitar la toma de datos
    if CONT < FRAME_LIMIT_FOR_DATA:
        population_history_fit.append(len(organisms))
        predator_population_history_fit.append(len(predators))
    
    population_history.append(len(organisms))
    predator_population_history.append(len(predators))
    
    CONT += 1

    font = pygame.font.Font(None, 24)
    text = font.render(f"Organismos: {len(organisms)} | Depredadores: {len(predators)} | Recursos: {len(resources)}", True, BLACK)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)   

pygame.quit()

# Calcular y mostrar la vida media de organismos
if organism_lifespans:
    average_organism_lifespan = sum(organism_lifespans) / len(organism_lifespans)
    print(f"Vida media de organismos: {average_organism_lifespan:.2f} frames")
else:
    print("No hubo datos suficientes para calcular la vida media de organismos.")

# Calcular y mostrar la vida media de depredadores
if predator_lifespans:
    average_predator_lifespan = sum(predator_lifespans) / len(predator_lifespans)
    print(f"Vida media de depredadores: {average_predator_lifespan:.2f} frames")
else:
    print("No hubo datos suficientes para calcular la vida media de depredadores.")

# Mostrar la gráfica con eventos
plot_population_history()

import numpy as np
from scipy.integrate import odeint
from scipy.optimize import minimize

# Función de Lotka-Volterra
def lotka_volterra(y, t, r, a, b, d):
    N, P = y
    dNdt = r * N - a * N * P
    dPdt = b * N * P - d * P
    return [dNdt, dPdt]

# Resolver el sistema de ecuaciones para un conjunto de parámetros
def solve_lotka_volterra(t, N0, P0, r, a, b, d):
    y0 = [N0, P0]
    params = (r, a, b, d)
    sol = odeint(lotka_volterra, y0, t, args=params)
    return sol[:, 0], sol[:, 1]  # Retorna presas y depredadores

def fit_lotka_volterra_optimized(t, N0, P0, N_data, P_data):
    def loss(params):
        r, a, b, d = params
        N_model, P_model = solve_lotka_volterra(t, N0, P0, r, a, b, d)
        error_N = np.mean((N_model - N_data) ** 2)
        error_P = np.mean((P_model - P_data) ** 2)
        return error_N + error_P

    # Condiciones iniciales 
    initial_guess = [0.5, 0.02, 0.02, 0.5]
    bounds = [(0, 1), (0, 1), (0, 1), (0, 1)]

    # Ajuste 
    result = minimize(loss, initial_guess, bounds=bounds, method="Powell")
    return result.x  # Retorna r, a, b, d


# Preparar los datos simulados
time = np.arange(len(population_history_fit))
N_data = np.array(population_history_fit)
P_data = np.array(predator_population_history_fit)
N0 = N_data[0]  # Población inicial de presas
P0 = P_data[0]  # Población inicial de depredadores

# Submuestreo de datos (tomar 1 de cada 10 frames)
sampling_rate = 10
time_sampled = time[::sampling_rate]
N_data_sampled = N_data[::sampling_rate]
P_data_sampled = P_data[::sampling_rate]

# Normalización de los datos
N_data_normalized = N_data / max(N_data)
P_data_normalized = P_data / max(P_data)
N0_normalized = N0 / max(N_data)
P0_normalized = P0 / max(P_data)

time_norm = (time)/(average_organism_lifespan/10) # Normalización con tiempo característico
time_sampled_norm = time_norm[::sampling_rate]

# Ajustar los parámetros con datos submuestreados
r, a, b, d = fit_lotka_volterra_optimized(time_sampled_norm, N0_normalized, P0_normalized, 
                                          N_data_sampled / max(N_data), 
                                          P_data_sampled / max(P_data))

# Resolver el modelo ajustado con todos los datos
N_fit_normalized, P_fit_normalized = solve_lotka_volterra(time_norm, N0_normalized, P0_normalized, r, a, b, d)

# Desnormalizar los resultados
N_fit = N_fit_normalized * max(N_data)
P_fit = P_fit_normalized * max(P_data)

# Mostrar los resultados
print(f"Parámetros ajustados:")
print(f"Tasa de crecimiento de presas (r): {r:.4f}")
print(f"Tasa de captura (a): {a:.4f}")
print(f"Tasa de conversión (b): {b:.4f}")
print(f"Tasa de muerte de depredadores (d): {d:.4f}")

# Graficar los resultados
plt.figure(figsize=(12, 6))
plt.plot(time, N_data, label="Presas (simuladas)", color="blue")
plt.plot(time, P_data, label="Depredadores (simulados)", color="red")
plt.plot(time, N_fit, "--", label="Presas (Lotka-Volterra)", color="blue")
plt.plot(time, P_fit, "--", label="Depredadores (Lotka-Volterra)", color="red")
plt.xlim(0,FRAME_LIMIT_FOR_DATA)
plt.xlabel("Tiempo " + r"($game~ticks$)")
plt.ylabel("Población")
plt.legend()
plt.grid(True)
plt.show()
