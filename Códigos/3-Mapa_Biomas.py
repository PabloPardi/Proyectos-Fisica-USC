# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 16:48:43 2024

@author: Usuario
"""
import pygame
import numpy as np
import noise
import matplotlib.pyplot as plt

# Configuración inicial
WIDTH, HEIGHT = 1200, 700
CELL_SIZE = 3
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

# Colores de biomas
COLORS = {
    "deep_water": (0, 0, 128), #Aguas profundas
    "shallow_water": (0, 0, 255), #Aguas superficiales
    "beach": (194, 178, 128),#Playa
    "meadow": (34, 139, 34), #Pradera
    "forest": (0, 100, 0), #Bosque
    "mountain": (139, 137, 137), #Montaña
    "snow": (255, 250, 250), #Nieve
}

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mundo Procedural Biofísico")

# Creamos la función de ruido Perlin
def generate_perlin_world(grid_width, grid_height, scale=80):
    world = np.zeros((grid_width, grid_height)) #Matriz del tamaño de la ventana
    seed = np.random.randint(0, 100)  # Semilla aleatoria
    for x in range(grid_width):
        for y in range(grid_height):
            world[x][y] = noise.pnoise2(
                x / scale, #Coordenadas escaladas 
                y / scale,
                octaves=6, #Octavas o capas de ruido
                persistence=0.5, #Reduce la amplitud
                lacunarity=2.0, #Aumenta la frecuencia
                repeatx=grid_width,
                repeaty=grid_height,
                base=seed,
            )
    # Normalizar valores entre 0 y 1
    min_val = world.min()
    max_val = world.max()
    if max_val - min_val > 0:
        world = (world - min_val) / (max_val - min_val)
    else:
        world.fill(0.5)
    return world

#Función para el cálculo de la temperatura y humedad que graficaremos posteriormente
def calculate_temperature_and_humidity(world, grid_width, grid_height):
    
    temperature = np.zeros_like(world)
    humidity = np.zeros_like(world)
    
    # Parámetros
    T_sea_level = 20  # Temperatura al nivel del mar (°C)
    T_gradient = -6.5  # Gradiente térmico (°C por 1000m)
    H_sea_level = 100  # Humedad al nivel del mar (%)
    H_gradient = -15   # Gradiente de humedad (% por 1000m)
    max_depth = -2000  # Máxima profundidad del océano (m)
    max_altitude = 4000  # Máxima altitud de las montañas (m)
    
    # Reescalar altitudes a metros considerando el 0 de altitud como el nivel del mar
    altitudes = (world - 0.5) * (max_altitude - max_depth) + (max_altitude + max_depth) / 2

    for y in range(grid_height):
        for x in range(grid_width):
            altitud = altitudes[x, y]  # Altitud real en metros
            
            # Cálculo de temperatura
            if altitud < 0:  # Bajo el nivel del mar (agua)
                temperature[x, y] = T_sea_level - (altitud / max_depth) * 18  # Agua más fría en profundidades
            elif altitud == 0:
                temperature[x, y] = T_sea_level #Temperatura al nivel del mar
            elif altitud > 0:
                temperature[x, y] = T_sea_level - (altitud / 1000) * abs(T_gradient) #Descenso de temperatura con el aumento de altitud
                
            # Cálculo de humedad
            if altitud < 0:  
                humidity[x, y] = 100  # Alta humedad en el agua
            else:  
                humidity[x, y] = max(0, H_sea_level + (altitud / 1000) * H_gradient) #Descenso con el aumento de altitud

    return temperature, humidity


# Determinar biomas basados en altitud, temperatura y humedad

def assign_biomes(world, temperature, humidity):
    biomes = np.empty(world.shape, dtype=object)

    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            altitud = world[x, y]
            temp = temperature[x, y]
            hum = humidity[x, y]
            
            # Asignar biomas
            if altitud < 0.2:  # Aguas profundas
                biomes[x, y] = "deep_water"
            elif altitud < 0.4:  # Aguas superficiales
                biomes[x, y] = "shallow_water"
            elif altitud < 0.43:  # Playas
                biomes[x, y] = "beach"
            elif altitud < 0.5 and hum > 50:  # Praderas
                biomes[x, y] = "meadow"
            elif altitud < 0.8 and hum > 70 and temp > 10:  # Bosques (requieren más humedad y temperatura moderada)
                biomes[x, y] = "forest"
            elif altitud < 0.9:  # Montañas
                biomes[x, y] = "mountain"
            else:  
                biomes[x, y] = "snow" # Zonas de nieve

    return biomes


# Dibujar el mapa en función de los biomas asignados
def draw_world_to_surface(biomes):
    surface = pygame.Surface((WIDTH, HEIGHT))
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            biome = biomes[x, y]
            color = COLORS[biome]
            pygame.draw.rect(surface, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    return surface

# Creamos el mapa
world = generate_perlin_world(GRID_WIDTH, GRID_HEIGHT)
temperature, humidity = calculate_temperature_and_humidity(world, GRID_WIDTH, GRID_HEIGHT)
biomes = assign_biomes(world, temperature, humidity)
world_surface = draw_world_to_surface(biomes)


# Bucle principal de Pygame
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Mostrar el mundo generado
    screen.fill((0, 0, 0))
    screen.blit(world_surface, (0, 0))
    pygame.display.flip()

#Generamos las gráficas
# Escalamos la altitud a metros
altitud_metros = (world - 0.5) * (4000 - (-2000)) + (4000 + (-2000)) / 2

# Crear graficas
#Gráfica de altitud
plt.figure(figsize=(12, 7))
plt.title("Mapa de Altitud (m)")
plt.imshow(altitud_metros.T, origin='upper', cmap='terrain', extent=[0, WIDTH, 0, HEIGHT]) 
plt.colorbar(label='Altitud (m)')
plt.xlabel('X')
plt.ylabel('Y')
plt.tight_layout()

#Gráfica de temperatura
plt.figure(figsize=(12, 7))
plt.title("Mapa de Temperatura (°C)")
plt.imshow(temperature.T, origin='upper', cmap='jet', extent=[0, WIDTH, 0, HEIGHT])
plt.colorbar(label='Temperatura (°C)')
plt.xlabel('X')
plt.ylabel('Y')
plt.tight_layout()

#Gráfica de humedad
plt.figure(figsize=(12,7))
plt.title("Mapa de Humedad (%)")
plt.imshow(humidity.T, origin='upper', cmap='Blues',extent=[0, WIDTH, 0, HEIGHT])
plt.colorbar(label='Humedad (%)')
plt.xlabel('X')
plt.ylabel('Y')
plt.tight_layout()

pygame.quit()
