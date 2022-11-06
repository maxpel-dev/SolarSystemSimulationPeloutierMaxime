import api
import sys
import pygame
import math

pygame.init()
w,h = 1024, 768
screen = pygame.display.set_mode((w,h))

# Vitesse de la simulation en jours/seconde
SPEED_MULTIPLIERS = [0.1, 0.2, 0.5, 1, 2, 5, 10, 100, 500]
speedMultiplierIndex = 0
FRAMERATE = 60
# Nom et couleurs des planètes du système solaire à inclure dans la simulation
BODIES = [ 
    {"Sun", (255, 255, 255)},
    {"Mercury", (255, 255, 255)}, 
    {"Venus", (255, 255, 255)},
    {"Earth", (255, 255, 255)},
    {"Mars", (255, 255, 255)},
    {"Jupiter", (255, 255, 255)},
    {"Saturn", (255, 255, 255)},
    {"Uranus", (255, 255, 255)},
    {"Neptune", (255, 255, 255)}
]

#Echelles
DISTANCE_SCALE = 1/5
SUN_SCALE = 1/100000
PLANET_SCALE = 1/100
SATELLITE_SCALE = 1/5000

# Les valeurs des attributs sont ramenées aux échelles définies dans les constantes.
class Planet:
    name = ""
    distanceFromSun = 0
    radius = 0
    orbitPercentage = 0
    daysPerOrbit = 0
    color = (255, 255, 255)
    x = 0
    y = 0

    def __init__(self, name, color):
        self.name = name
        self.color = color
        data = api.GetPlanetData(name)

        # Distance du soleil : "semimajorAxis"
        # Rayon : "meanRadius"
        # Jours par orbite = "sideralOrbit"
        # Jours par rotation sur elle-même = "sideralRotation"
        self.daysPerOrbit = data["sideralOrbit"]
        self.distanceFromSun = data["meanRadius"]*DISTANCE_SCALE
        self.radius = data["meanRadius"]*PLANET_SCALE
        self.angle = 0
        self.updatePosition()
        print(str(self))
    
    def __str__(self):
        s = ""
        s += "Name : " + str(self.name) + "\n"
        s += "Coordinates : " + str(self.x) + " " + str(self.y) + "\n"
        s += "Orbit % : " + str(self.orbitPercentage) + "\n"
        #s += "Radius : " + str(self.radius) + "\n"
        s += "Angle : " + str(self.angle) + "\n"
        return s

    def refresh(self):
        self.updatePosition()
        self.draw()

    def updatePosition(self):
        self.orbitPercentage += SPEED_MULTIPLIERS[speedMultiplierIndex]/self.daysPerOrbit
        self.angle = (2*math.pi)*self.orbitPercentage
        self.x = (self.distanceFromSun*math.cos(self.angle))*DISTANCE_SCALE + w/2
        self.y = (self.distanceFromSun*math.sin(self.angle))*DISTANCE_SCALE + h/2
    
    def draw(self):
        #print(str(self))
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

play = True
clock = pygame.time.Clock()


screen.fill((0,0,0))
p = Planet("Mercury", (255, 255, 255))

while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
        if event.type == pygame.MOUSEMOTION:
            pass
            # print(event.pos)
        if event.type == pygame.KEYUP:
            print(event.key, event.unicode, event.scancode)
            if event.key == pygame.K_ESCAPE:
                play = False
            #Réglage de vitesse
            if event.key == pygame.K_UP or event.key == pygame.K_z:
                pass
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                pass

    screen.fill((0,0,0))
    p.refresh()
    clock.tick(FRAMERATE)
    pygame.display.flip()