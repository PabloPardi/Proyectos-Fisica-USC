'''
El clock.tick de la simulación ha sido establecido a 1000 para realizar las 
simulaciones. Por defecto viene configurado para ser igual a los FPS.
'''

import pygame
import sys
import math
import random
import matplotlib.pyplot as plt


WIDTH, HEIGHT = 1000, 700
CRUST_HEIGHT = 50
CRUST_Y = HEIGHT - CRUST_HEIGHT

VOLCANO_X = WIDTH // 2
VOLCANO_TOP = CRUST_Y - 80

STAGE_0_DURATION = 500
STAGE_1_DURATION = 1500
FPS = 60
time_steps = 0

COLOR_H2O = (0, 120, 255)
COLOR_CO2 = (100, 100, 100)
COLOR_S   = (255, 255, 0)   
COLOR_N2  = (220, 220, 0)
COLOR_O2  = (76, 255, 204)
COLOR_CH4 = (255,165,0)
COLOR_SO2 = (153,50,204)
COLOR_H2  = (255, 0, 0)
COLOR_He  = (0, 255, 0)
COLOR_ROCK = (170,170,170)

OCEAN_COLOR = COLOR_H2O
ocean_thickness = 0

VOLCANO_COLOR = (120,60,30)
VOLCANO_LAVA = (255,69,0)

O2_THRESHOLD = 21.0

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Atmósfera - Mantener partículas, concentraciones estables")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 18)

GAS_COMPOSITION_STAGE_0 = {
    'H2': 0.9,
    'He': 0.1
}

GAS_COMPOSITION_STAGE_1 = {
    'CO2': 0.4,
    'H2O': 0.54,
    'N2': 0.03,
    'CH4':0.015,
    'SO2':0.015
}

class Particle:
    def __init__(self, x, y, vx, vy, gas_type, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.gas_type = gas_type
        self.color = color
        self.radius = 2
        self.settled = False

    def update(self, stage, elapsed_stage2):
        if stage == 2 and self.gas_type == 'H2O' and not self.settled:
            # Incrementar la probabilidad de precipitación y que crezca más rápido
            precipitation_prob = min(0.0005 + elapsed_stage2*1e-6, 0.002) 
            if random.random() < precipitation_prob:
                self.vy = 0.5

        self.x += self.vx
        self.y += self.vy

        if stage == 2 and self.gas_type == 'H2O' and not self.settled and self.y > CRUST_Y - ocean_thickness:
            self.y = CRUST_Y - ocean_thickness
            self.vx = 0
            self.vy = 0
            self.settled = True
        else:
            if self.x < 0:
                self.x = 0
                self.vx = -self.vx
            if self.x > WIDTH:
                self.x = WIDTH
                self.vx = -self.vx
            if self.y < 0:
                if self.gas_type not in ['H2','He']:
                    self.y = 0
                    self.vy = -self.vy
            if self.y > CRUST_Y - ocean_thickness and not self.settled:
                self.y = CRUST_Y - ocean_thickness
                self.vy = -abs(self.vy)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 5
        self.color = (10, 120, 10)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

class MineralDeposit:
    def __init__(self, x, radius):
        self.x = x
        self.y = CRUST_Y
        self.radius = radius

    def draw(self, screen):
        pygame.draw.circle(screen, COLOR_ROCK, (int(self.x), int(self.y)), self.radius)

def check_collision(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    dist = math.hypot(dx, dy)
    return dist < (p1.radius + p2.radius)

particles = []
cells = []
mineral_deposits = []

def generate_initial_stage_0_particles(num=2000):
    for _ in range(num):
        x = random.uniform(0, WIDTH)
        y = random.uniform(0, CRUST_Y)
        r = random.random()
        cumulative = 0
        gas_type = None
        for g, perc in GAS_COMPOSITION_STAGE_0.items():
            cumulative += perc
            if r <= cumulative:
                gas_type = g
                break
        color = COLOR_H2 if gas_type == 'H2' else COLOR_He
        vx = random.uniform(-0.5,0.5)
        vy = -abs(random.uniform(0.5,1.5))
        p = Particle(x,y,vx,vy,gas_type,color)
        particles.append(p)

def emit_gases(stage):
    if stage != 1:
        return
    comp = GAS_COMPOSITION_STAGE_1
    speed = random.uniform(2,4)
    angle = random.uniform(-math.pi/4, math.pi/4)
    vx = speed*math.sin(angle)
    vy = -abs(speed*math.cos(angle))
    r = random.random()
    cumulative=0
    gas_type=None
    for g,perc in comp.items():
        cumulative+=perc
        if r<=cumulative:
            gas_type=g
            break

    if gas_type=='H2O':
        color=COLOR_H2O
    elif gas_type=='CO2':
        color=COLOR_CO2
    elif gas_type=='N2':
        color=COLOR_N2
    elif gas_type=='CH4':
        color=COLOR_CH4
    elif gas_type=='SO2':
        color=COLOR_SO2
    else:
        color=(255,255,255)

    p=Particle(VOLCANO_X,VOLCANO_TOP,vx,vy,gas_type,color)
    particles.append(p)

def form_ocean():
    settled_count = sum(1 for p in particles if p.gas_type == 'H2O' and p.settled)
    global ocean_thickness
    # Incrementar el crecimiento del océano
    if settled_count > 0:
        ocean_thickness += 0.03  

    # Eliminar más partículas asentadas por ciclo para acelerar la desaparición del agua gas
    max_particles_to_remove = random.randint(3,5) 
    removed = 0
    new_list = []
    for p in particles:
        if p.gas_type == 'H2O' and p.settled and removed < max_particles_to_remove:
            removed += 1
        else:
            new_list.append(p)
    return new_list

def calculate_o2_concentration(particles):
    o2_count = sum(1 for p in particles if p.gas_type=='O2')
    total = len(particles)
    return (o2_count/total*100.0) if total>0 else 0.0

def count_gases(particles):
    counts={'H2':0,'He':0,'H2O':0,'CO2':0,'N2':0,'O2':0,'CH4':0,'SO2':0}
    for p in particles:
        if p.gas_type in counts:
            counts[p.gas_type]+=1
    total=sum(counts.values())
    percentages={}
    if total>0:
        for g in counts:
            percentages[g]=(counts[g]/total)*100.0
    else:
        for g in counts:
            percentages[g]=0.0
    return percentages, counts, total

stage=0
ocean_formed=False
o2_production_enabled=True

generate_initial_stage_0_particles(num=2000)

CELL_START_DELAY=300
CELL_SPAWN_INTERVAL=60
MAX_CELLS=30
cells_spawned=0

co2_disappear_probability=0.0005
ch4_disappear_probability=0.002
so2_disappear_probability=0.002

mineral_deposits_count = 0

# Variables adicionales para el registro de concentraciones
gas_evolution = {'time': [], 'H2': [], 'He': [], 'H2O': [], 'CO2': [], 'N2': [], 'O2': [], 'CH4': [], 'SO2': []}

running=True
while running:
    dt=clock.tick(FPS)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

    # Avanzar etapa 
    if stage==0 and time_steps>=STAGE_0_DURATION:
        stage=1
    elif stage==1 and time_steps>=STAGE_0_DURATION+STAGE_1_DURATION:
        stage=2

    # Calcular el tiempo transcurrido en etapa 2
    elapsed_stage2 = 0
    if stage==2:
        elapsed_stage2 = time_steps - (STAGE_0_DURATION+STAGE_1_DURATION)

    if stage==1:
        # Emitir gases en etapa 1
        for _ in range(10):
            emit_gases(stage)

    particles_to_remove=[]
    for p in particles:
        p.update(stage, elapsed_stage2)
        if (p.gas_type in ['H2','He']) and p.y<0:
            particles_to_remove.append(p)
    for pr in particles_to_remove:
        particles.remove(pr)

    if stage >= 1:
        new_particles = []
        for p in particles:
            vanish = False
            if p.gas_type == 'SO2' and random.random() < so2_disappear_probability:
                vanish = True
            elif p.gas_type == 'CH4' and random.random() < ch4_disappear_probability:
                vanish = True
            if not vanish:
                new_particles.append(p)
        particles = new_particles

    # Ajustes en etapa 2: formación de océano
    if stage == 2:
        particles = form_ocean()
        gas_percentages, counts, total = count_gases(particles)
        h2o_in_air = any(p.gas_type == 'H2O' and not p.settled for p in particles)
        # Mantener etapa 2 hasta que el porcentaje de H2O gas sea <= 1%
        if not h2o_in_air and gas_percentages['H2O'] <= 1.0:
            stage = 3
            ocean_formed = True

    gas_percentages, counts, total = count_gases(particles)   
         
    if stage >= 2:
        new_particles = []
        co2_vanished = 0
        for p in particles:
            vanish = (p.gas_type == 'CO2' and random.random() < co2_disappear_probability)
            if vanish:
                co2_vanished += 0.5
            else:
                new_particles.append(p)
        particles = new_particles
        if co2_vanished>0:
            x = random.uniform(0, WIDTH)
            radius = 2 + co2_vanished
            mineral_deposits.append(MineralDeposit(x, radius))
        mineral_deposits_count += co2_vanished

        # Ajuste N2
        desired_n2_min = 77.5
        desired_n2_max = 80.0
        desired_n2 = 78.0 
    
        n2_current = gas_percentages['N2']
    
        if n2_current < desired_n2_min or n2_current > desired_n2_max:
            desired_n2_count = int((desired_n2 / 100) * total)
            current_n2_count = counts['N2']
            max_step = 2
    
            if n2_current < desired_n2_min:
                diff = desired_n2_min - n2_current
                scaled_diff = int(diff * total / 200)  
                scaled_diff = max(scaled_diff, 1)  
                to_add = min(desired_n2_count - current_n2_count, scaled_diff, max_step)
    
                for _ in range(to_add):
                    x = random.uniform(0, WIDTH)
                    y = random.uniform(0, CRUST_Y)
                    vx, vy = random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)
                    particles.append(Particle(x, y, vx, vy, 'N2', COLOR_N2))
    
            elif n2_current > desired_n2_max:
                diff = n2_current - desired_n2_max
                scaled_diff = int(diff * total / 200)
                scaled_diff = max(scaled_diff, 1)
                to_remove = min(counts['N2'] - desired_n2_count, scaled_diff, max_step)
    
                newp = []
                for p in particles:
                    if to_remove > 0 and p.gas_type == 'N2':
                        to_remove -= 1
                    else:
                        newp.append(p)
                particles = newp  
    
    if stage==3:
        if time_steps>CELL_START_DELAY and cells_spawned<MAX_CELLS:
            if (time_steps-CELL_START_DELAY)%CELL_SPAWN_INTERVAL==0:
                ocean_y=CRUST_Y - ocean_thickness
                x=random.uniform(0,WIDTH)
                y=ocean_y+5
                cells.append(Cell(x,y))
                cells_spawned+=1
        
        for c in cells:
            for p in particles:
                if p.gas_type=='CO2' and check_collision(c,p):
                    if o2_production_enabled and random.random()<1:# podemos ajustar la producción de O2
                        px,py=p.x,p.y
                        vx,vy=random.uniform(-0.5,0.5),random.uniform(-0.5,-1)
                        particles.append(Particle(px,py,vx,vy,'O2',COLOR_O2))
                    break

        o2_concentration=calculate_o2_concentration(particles)
        if o2_concentration>=O2_THRESHOLD:
            o2_production_enabled=False

        if total>0:
            desired_h2o=1
            w_current=gas_percentages['H2O']
            if abs(w_current - desired_h2o)>0.0001:
                desired_h2o_count=int((desired_h2o/100)*total)
                current_h2o_count=counts['H2O']
                step=2
                if current_h2o_count>desired_h2o_count:
                    to_remove=min(current_h2o_count-desired_h2o_count,step)
                    newp=[]
                    for p in particles:
                        if to_remove>0 and p.gas_type=='H2O':
                            to_remove-=1
                        else:
                            newp.append(p)
                    particles=newp
                elif current_h2o_count<desired_h2o_count:
                    to_add=min(desired_h2o_count-current_h2o_count,step)
                    for _ in range(to_add):
                        x=random.uniform(0,WIDTH)
                        y=random.uniform(0,CRUST_Y)
                        vx,vy=random.uniform(-0.5,0.5),random.uniform(-0.5,0.5)
                        particles.append(Particle(x,y,vx,vy,'H2O',COLOR_H2O))
                gas_percentages, counts, total = count_gases(particles)

            # CO2 >=1%
            if gas_percentages['CO2']<1.0:
                desired_co2=1.0
                desired_co2_count=int((desired_co2/100)*total)
                current_co2_count=counts['CO2']
                step=2
                to_add=min(desired_co2_count-current_co2_count,step)
                for _ in range(to_add):
                    x=random.uniform(0,WIDTH)
                    y=random.uniform(0,CRUST_Y)
                    vx,vy=random.uniform(-0.5,0.5),random.uniform(-0.5,0.5)
                    particles.append(Particle(x,y,vx,vy,'CO2',COLOR_CO2))
                gas_percentages, counts, total = count_gases(particles)

    gas_percentages, counts, total = count_gases(particles)
    gas_evolution['time'].append(time_steps)
    for gas in gas_evolution.keys():
        if gas != 'time':
            gas_evolution[gas].append(gas_percentages[gas])

    # Dibujar
    screen.fill((0,0,30))
    pygame.draw.rect(screen,(139,69,19),(0,CRUST_Y,WIDTH,CRUST_HEIGHT))

    if stage>=1:
        pygame.draw.polygon(screen,VOLCANO_COLOR,[(VOLCANO_X-30,CRUST_Y),(VOLCANO_X,VOLCANO_TOP),(VOLCANO_X+30,CRUST_Y)])
        if stage==1:
            pygame.draw.polygon(screen,VOLCANO_LAVA,[(VOLCANO_X-5,VOLCANO_TOP+10),(VOLCANO_X,VOLCANO_TOP),(VOLCANO_X+5,VOLCANO_TOP+10)])

    if ocean_thickness>0:
        ocean_y=CRUST_Y - ocean_thickness
        pygame.draw.rect(screen,OCEAN_COLOR,(0,ocean_y,WIDTH,ocean_thickness))
        pygame.draw.line(screen,(200,200,200),(0,ocean_y),(WIDTH,ocean_y),1)

    for p in particles:
        p.draw(screen)
    for rock in mineral_deposits:
        rock.draw(screen)
    if stage==3:
        for c in cells:
            c.draw(screen)

    gas_percentages, counts, total = count_gases(particles)
    text_lines=[]
    for g in ['H2','He','H2O','CO2','N2','O2','CH4','SO2']:
        text_lines.append(f"{g}: {gas_percentages[g]:.2f}%")
    text_lines.append(f"Depositos minerales: {len(mineral_deposits)}")

    # Dibujar la etapa actual en pantalla con un marco oscuro
    stage_text = f"Etapa: {stage}"
    stage_surface = font.render(stage_text, True, (255, 255, 255))
    
    # Tamaño del texto y posición
    text_width, text_height = stage_surface.get_size()
    padding = 10
    stage_box_width = text_width + padding * 2
    stage_box_height = text_height + padding
    stage_box_x = 10
    stage_box_y = 10
    
    # Crear el marco oscuro
    stage_box = pygame.Surface((stage_box_width, stage_box_height))
    stage_box.set_alpha(200)
    stage_box.fill((50, 50, 50))
    
    # Dibujar el marco y el texto
    screen.blit(stage_box, (stage_box_x, stage_box_y))
    screen.blit(stage_surface, (stage_box_x + padding, stage_box_y + padding // 2))

    box_width=300
    box_height=len(text_lines)*20+10
    x_pos=WIDTH-box_width-10
    y_pos=10
    s=pygame.Surface((box_width,box_height))
    s.set_alpha(200)
    s.fill((50,50,50))
    screen.blit(s,(x_pos,y_pos))

    y_offset=y_pos+5
    for line in text_lines:
        t_surf=font.render(line,True,(255,255,255))
        screen.blit(t_surf,(x_pos+10,y_offset))
        y_offset+=20

    pygame.display.flip()
    time_steps+=1

pygame.quit()

def norm_color(c):
    return (c[0]/255.0, c[1]/255.0, c[2]/255.0)

gas_colors = {
    'H2': norm_color(COLOR_H2),
    'He': norm_color(COLOR_He),
    'H2O': norm_color(COLOR_H2O),
    'CO2': norm_color(COLOR_CO2),
    'N2': norm_color(COLOR_N2),
    'O2': norm_color(COLOR_O2),
    'CH4': norm_color(COLOR_CH4),
    'SO2': norm_color(COLOR_SO2)
}

plt.figure(figsize=(10,6))
for gas in ['H2','He','H2O','CO2','N2','O2','CH4','SO2']:
    plt.plot(gas_evolution['time'], gas_evolution[gas], label=gas, color=gas_colors[gas])

plt.xlabel("Tiempo " + r"($game~ticks$)")
plt.ylabel('Concentración atmosférica (%)')
plt.ylim(0,100)
plt.xlim(-460,8000)

# ETAPA 0
x_line_0 = 500
plt.axvline(x=x_line_0, color='black', linestyle='--', linewidth=0.8, label=None)
plt.text(x_line_0-110, 92, 'Etapa 0', 
         horizontalalignment='right', verticalalignment='bottom', color='black', fontsize=12)

# ETAPA 1
x_line_1 = 2000
plt.axvline(x=x_line_1, color='black', linestyle='--', linewidth=0.8, label=None)
plt.text(x_line_1-370, 92, 'Etapa 1', 
         horizontalalignment='right', verticalalignment='bottom', color='black', fontsize=12)

# ETAPA 2
x_line_2 = 4000
plt.axvline(x=x_line_2, color='black', linestyle='--', linewidth=0.8, label=None)
plt.text(x_line_2-650, 92, 'Etapa 2', 
         horizontalalignment='right', verticalalignment='bottom', color='black', fontsize=12)

# ETAPA 3
x_line_3 = 10000
plt.axvline(x=x_line_3, color='black', linestyle='--', linewidth=0.8, label=None)
plt.text(x_line_3-3650, 92, 'Etapa 3', 
         horizontalalignment='right', verticalalignment='bottom', color='black', fontsize=12)

plt.title('Evolución de la composición atmosférica a lo largo del tiempo')

plt.legend(loc='center right')

# Guardar como PDF
plt.savefig("ATM_grafico_gases.pdf", format='pdf')

plt.grid(True)
plt.show()

sys.exit()
