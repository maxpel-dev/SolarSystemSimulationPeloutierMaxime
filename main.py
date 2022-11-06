import api
import pygame
import math

pygame.init()
w,h = 1520, 768
screen = pygame.display.set_mode((w,h))
displayPlanetOrbits = True

SUN_X, SUN_Y = 230, h/2
SUN_COLOR = (235, 158, 26)
# Echelles - Vous pouvez vous amuser à jouer avec, je pense avoir trouvé un bon équilibre entre précision et qualité d'affichage
DISTANCE_SCALE = 1/1600
SUN_SCALE = 1/5000
PLANET_SCALE = SUN_SCALE*6
SATELLITE_SCALE = 1/5000
PLANET_ORBIT_OFFSET = 42/SUN_SCALE # Distance fixe ajoutée à la distance entre le soleil et chaque planète pour éviter que les planètes proches du soleil se fassent "manger"
# Vitesse de la simulation
SPEED_MULTIPLIERS = [0.5, 1, 2, 5, 10, 50, 100, 250, 500, 1000, 5000]
speedMultiplierIndex = 4
FRAMERATE = 165
# Nom et couleurs des planètes du système solaire à inclure dans la simulation
PLANETS = [ 
    ("Mercury", (240, 198, 144)),
    ("Venus", (237, 146, 26)),
    ("Earth", (89, 149, 240)),
    ("Mars", (237, 68, 38)),
    ("Jupiter", (201, 123, 81)),
    ("Saturn", (230, 158, 119)),
    ("Uranus", (195, 231, 250)),
    ("Neptune", (11, 67, 179))
    # Désolé Pluton, t'es pas tout à fait une planète et puis ça fait trop loin :(
]

# Les valeurs des attributs sont ramenées aux échelles définies dans les constantes.
class CelestialBody:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        data = api.GetCelestailBodyData(self.name)

        # Distance du soleil : "semimajorAxis"
        # Rayon : "meanRadius"
        # Jours par orbite = "sideralOrbit"
        # Jours par rotation sur soi-même = "sideralRotation" (inutilisé actuellement)
        self.daysPerOrbit = data["sideralOrbit"]
        self.distanceFromOrbitCenter = data["semimajorAxis"]*DISTANCE_SCALE + PLANET_ORBIT_OFFSET
        self.radius = data["meanRadius"]*PLANET_SCALE
        self.updatePosition()
        print(str(self))
    
    def __str__(self):
        s = ""
        s += "Nom : " + str(self.name) + "\n"
        s += "Coordonnées (x, y) : " + str(self.x) + ", " + str(self.y) + "\n"
        return s

    def refresh(self):
        self.draw()

    def updatePosition(self, parent_x = SUN_X, parent_y = SUN_Y):
        self.orbitCount += (SPEED_MULTIPLIERS[speedMultiplierIndex]/FRAMERATE)/self.daysPerOrbit
        self.angle = (2*math.pi)*self.orbitCount
        self.x = (self.distanceFromOrbitCenter*math.cos(self.angle))*DISTANCE_SCALE + parent_x
        self.y = (self.distanceFromOrbitCenter*math.sin(self.angle))*DISTANCE_SCALE + parent_y
    
    def draw(self):
        # print(str(self))
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

class Planet(CelestialBody):
    def __init__(self, name, color):
        self.angle = 0
        self.orbitCount = 0
        super().__init__(name, color)
        self.satellites = []
        # TODO ajouter les satellites à chaque planète

    def __str__(self):
        s = super().__str__()
        s += "Nombre d'orbites : " + str(self.orbitCount) + "\n"
        s += "Angle : " + str(self.angle) + "\n"
        return s

    def refresh(self):
        self.updatePosition()
        if displayPlanetOrbits:
            self.drawOrbit()
        super().draw()

    def updatePosition(self, relative_x = SUN_X, relative_y = SUN_Y):
        self.orbitCount += (SPEED_MULTIPLIERS[speedMultiplierIndex]/FRAMERATE)/self.daysPerOrbit
        self.angle = (2*math.pi)*self.orbitCount
        self.x = (self.distanceFromOrbitCenter*math.cos(self.angle))*DISTANCE_SCALE + relative_x
        self.y = (self.distanceFromOrbitCenter*math.sin(self.angle))*DISTANCE_SCALE + relative_y

    def drawOrbit(self):
        pygame.draw.circle(screen, (255, 255, 255), (SUN_X, SUN_Y), self.distanceFromOrbitCenter*DISTANCE_SCALE, 1)

class Sun(CelestialBody):
    def __init__(self):
        self.name = "Sun"
        self.color = SUN_COLOR
        data = api.GetCelestailBodyData(self.name)
        self.radius = data["meanRadius"]*SUN_SCALE
        self.planets = []
        for p in PLANETS:
            self.planets.append(Planet(p[0], p[1]))
        self.draw()

    # La simulation étant héliocentrique, pas besoin de recalculer la position du soleil
    def refresh(self):
        self.draw()
    
    def draw(self):
        pygame.draw.circle(screen, SUN_COLOR, (SUN_X, SUN_Y), self.radius)



play = True
clock = pygame.time.Clock()
screen.fill((0,0,0))

sun = Sun()

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
                if(speedMultiplierIndex < len(SPEED_MULTIPLIERS)-1): speedMultiplierIndex += 1
                print("Vitesse x" + str(SPEED_MULTIPLIERS[speedMultiplierIndex]))
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if(speedMultiplierIndex > 0): speedMultiplierIndex -= 1
                print("Vitesse x" + str(SPEED_MULTIPLIERS[speedMultiplierIndex]))
            # Affichage des orbites
            if event.key == pygame.K_p:
                displayPlanetOrbits = not displayPlanetOrbits


    screen.fill((0,0,0))
    # Rafraîchissement de l'affichage du système solaire
    for planet in sun.planets:
        planet.refresh()
    sun.refresh()

    clock.tick(FRAMERATE)
    pygame.display.flip()