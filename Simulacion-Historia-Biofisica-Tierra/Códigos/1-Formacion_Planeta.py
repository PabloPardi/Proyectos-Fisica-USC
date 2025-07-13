# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 10:24:09 2024

@author: Usuario
"""

import pygame
import sys
import math
import random
import matplotlib.pyplot as plt

# Configuración de la ventana 

WIDTH, HEIGHT = 1000, 750
CENTER = (WIDTH // 2, HEIGHT // 2)

# Constantes de la simulación

G = 0.5 #Constante de gravitación universal
star_mass = 300000  #Masa de la estrella
protoplanet_initial_mass = 10 #Masa del protoplaneta inicial
absorption_radius = 10 #Radio de absorción del protoplaneta
NUM_PARTICLES = 300 #Número de partículas
dt = 0.1
SUBSTEPS = 5
#Tasa de enfriamiento
COOLING_RATE =0.1

# Colores que utilizaremos
BLACK, WHITE, YELLOW, RED, BROWN = (0, 0, 0), (255, 255, 255), (255, 255, 0), (255, 50, 50), (128,64,0)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Formación del protoplaneta")
clock = pygame.time.Clock()

#Definimos las funciones necesarias dentro de una clase

class Particle:
    def __init__(self, x, y, vx, vy, mass, color=WHITE):
        self.x, self.y, self.vx, self.vy, self.mass = x, y, vx, vy, mass
        self.color = color
        self.energy_lost = 0  # Energía acumulada perdida

    #Dibujar las partículas
    def draw(self, screen):
        r = max(2, int(self.mass**0.5))
        #r = max(2, int(self.mass**(1/3)))
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), r)

    #Cálculo de distancia entre partículas
    def distance_to(self, other):
        return math.hypot(self.x - other.x, self.y - other.y)

    #Cálculo del momento lineal y la energía cinética de la colisión inelástica
    def add_momentum(self, other):
        # Conservación del momento lineal
        px = self.mass * self.vx + other.mass * other.vx
        py = self.mass * self.vy + other.mass * other.vy
        total_mass = self.mass + other.mass
    
        # Velocidades finales
        vx_final = px / total_mass
        vy_final = py / total_mass
    
        # Energía cinética inicial
        initial_kinetic_energy = (0.5 * self.mass * (self.vx**2 + self.vy**2) +
                                  0.5 * other.mass * (other.vx**2 + other.vy**2))
    
        # Energía cinética final
        final_kinetic_energy = 0.5 * total_mass * (vx_final**2 + vy_final**2)
    
        # Energía perdida
        energy_lost = initial_kinetic_energy - final_kinetic_energy
        self.energy_lost += energy_lost  # Energia acumulada (calor)
    
        # Actualizar propiedades del protoplaneta
        self.mass = total_mass
        self.vx, self.vy = vx_final, vy_final
    
        # Actualizar color en función de la energía perdida
        self.update_color()
        
        # Registrar la energía acumulada para graficar
        energy_accumulated.append(self.energy_lost)
    
    #Enfriamiento 
    def cool_down(self, dt):
        # Reducir energía acumulada gradualmente (enfriamiento)
        self.energy_lost = max(self.energy_lost - COOLING_RATE * dt, 0)
        self.update_color()  # Actualizar el color según la nueva energía acumulada
    
    #Cambio de color del protoplaneta
    def update_color(self):
        # Escalar el nivel de "calor" según la energía perdida acumulada
        heat_level = min(self.energy_lost / 1000, 1)  # Normalizar a [0, 1]
    
        # Transición de marrón a rojo
        red = int(139 + (255 - 139) * heat_level)  # Incrementa el rojo con el calor
        green = int(69 * (1 - heat_level))         # Disminuye el verde
        blue = int(19 * (1 - heat_level))          # Disminuye el azul
    
        self.color = (red, green, blue)

#Cálculo aceleración gravitatoria
def gravitational_acceleration(p1, p2, mass):
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    dist2 = dx**2 + dy**2 + 1e-12
    a = G * mass / dist2
    return a * dx / math.sqrt(dist2), a * dy / math.sqrt(dist2)

#Generamos las partículas
def initialize_particles():
    particles = []
    for _ in range(NUM_PARTICLES):
        r = random.uniform(300, 400) #Radio órbita
        ang = random.uniform(0, 2 * math.pi)
        x, y = CENTER[0] + r * math.cos(ang), CENTER[1] + r * math.sin(ang)
        v = math.sqrt(G * star_mass / r) 
        vx, vy = -v * math.sin(ang), v * math.cos(ang)
        particles.append(Particle(x, y, vx, vy, 1)) #Masa=1
    return particles

#Runge-Kutta de 4 orden
def runge_kutta_step(particle, ax_func):
    x, y, vx, vy = particle.x, particle.y, particle.vx, particle.vy

    def f(state, dt):
        x, y, vx, vy = state
        ax, ay = ax_func((x, y))
        return vx, vy, ax, ay

    # RK4
    k1 = f((x, y, vx, vy), 0)
    k2 = f((x + k1[0] * dt / 2, y + k1[1] * dt / 2, vx + k1[2] * dt / 2, vy + k1[3] * dt / 2), dt / 2)
    k3 = f((x + k2[0] * dt / 2, y + k2[1] * dt / 2, vx + k2[2] * dt / 2, vy + k2[3] * dt / 2), dt / 2)
    k4 = f((x + k3[0] * dt, y + k3[1] * dt, vx + k3[2] * dt, vy + k3[3] * dt), dt)

    dx = (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) * dt / 6
    dy = (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) * dt / 6
    dvx = (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2]) * dt / 6
    dvy = (k1[3] + 2 * k2[3] + 2 * k3[3] + k4[3]) * dt / 6

    particle.x += dx
    particle.y += dy
    particle.vx += dvx
    particle.vy += dvy

#Actualizar posiciones y velocidades
def update_positions_and_velocities(particles, big_particle):
    for p in particles + [big_particle]:
        runge_kutta_step(p, lambda pos: gravitational_acceleration(pos, CENTER, star_mass))

        if p is not big_particle:
            ax_big, ay_big = gravitational_acceleration((p.x, p.y), (big_particle.x, big_particle.y), big_particle.mass)
            p.vx += ax_big * dt
            p.vy += ay_big * dt

#Acreción de partículas por el protoplaneta si se encuentran dentro del radio de absorción
def absorb_particles(particles, big_particle):
    for p in particles[:]:
        if big_particle.distance_to(p) < absorption_radius + math.sqrt(p.mass):
            big_particle.add_momentum(p)
            particles.remove(p)

#------------------------------------------------------------------------------------------------------------------------

v_big_particle= math.sqrt(G * star_mass / 350) #Velocidad inicial del protoplaneta
protoplanet = Particle(CENTER[0] + 350, CENTER[1], 0, v_big_particle, protoplanet_initial_mass, BROWN)
particles = initialize_particles()

# Inicializa el tiempo y registra los valores para la gráfica
time = 0

# Lista para registrar la energía cinética perdida acumulada y el tiempo
time_points = []
energy_accumulated = []


running = True
while running:
    clock.tick(1000)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Subpasos de simulación
    for _ in range(SUBSTEPS):
        update_positions_and_velocities(particles, protoplanet)
        absorb_particles(particles, protoplanet)
    
    #Enfriamiento del protoplaneta con el tiempo
    protoplanet.cool_down(dt * SUBSTEPS)
        
    # Registrar energía acumulada y tiempo
    time += dt * SUBSTEPS
    time_points.append(time)
    
    # Asegurar que energy_accumulated crezca con time_points
    if len(energy_accumulated) < len(time_points):
        if energy_accumulated:
            energy_accumulated.append(energy_accumulated[-1])
        else:
            energy_accumulated.append(0)  # Valor inicial si aún no hay energía
            
    # Dibujar
    pygame.draw.circle(screen, YELLOW, CENTER, 30)
    for p in particles:
        p.draw(screen)
    protoplanet.draw(screen)

    pygame.display.flip()

pygame.quit()

# Generar la gráfica de energía acumulada vs tiempo
plt.figure(figsize=(10, 6))
plt.plot(time_points, energy_accumulated, label="Energía acumulada (calor)", color='red')
plt.title("Relación entre Calor acumulado y Tiempo")
plt.xlabel("Tiempo")
plt.ylabel("Energía Acumulada")
plt.legend()
plt.grid()
plt.show()

sys.exit()