import api
import pygame
import math

pygame.init()
w,h = 1520, 768
screen = pygame.display.set_mode((w,h))
displayPlanetOrbits = True
ENABLE_SATELLITES = False

BASE_URL = "https://api.le-systeme-solaire.net/rest.php/bodies/"
SUN_X, SUN_Y = 230, h/2
SUN_COLOR = (235, 158, 26)
# Echelles - Vous pouvez vous amuser à jouer avec, je pense avoir trouvé un bon équilibre entre précision et lisibilité d'affichage
DISTANCE_SCALE = 1/1600
SUN_SCALE = 1/5300
PLANET_SCALE = SUN_SCALE*6
SATELLITE_SCALE = 1/5000
PLANET_ORBIT_OFFSET = 42/SUN_SCALE # Distance fixe ajoutée à la distance entre le soleil et chaque planète pour éviter que les planètes proches du soleil se fassent "manger"
# Vitesse de la simulation
SPEED_MULTIPLIERS = [0.5, 1, 2, 5, 10, 50, 100, 250, 500, 1000, 5000]
speedMultiplierIndex = 4
FRAMERATE = 165
# ID (peut être différent du NOM, mais pas le cas ici) et couleurs des planètes du système solaire à inclure dans la simulation
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
SATELLITE_COLOR = (204, 204, 204)

class CelestialBody:
    """
    Considérez cette classe comme abstraite. Il s'agît de la classe de base des différents corps célestes affichés dans la simulation.\n
    """
    def __init__(self, id, color, initial_x = w/2, initial_y = h/2):
        self.x = initial_x
        self.y = initial_y
        self.id = id
        self.color = color
        # Les données de la réponse API sont temporairement stockées dans un attribut de l'objet
        # Pour que les objets des classes héritant de CelestailBody puissent y accéder en appelant le constructeur supérieur
        self.apiData = api.GetCelestialBodyDataFromId(self.id)
        self.radius = self.apiData["meanRadius"] # Les échelles sont appliquées dans les constructeurs des classes inférieures
        #print(str(self))
        self.draw()
    
    def __str__(self):
        s = ""
        s += "ID : " + str(self.id) + "\n"
        s += "Coordonnées (x, y) : " + str(self.x) + ", " + str(self.y) + "\n"
        return s
    
    def draw(self):
        # print(str(self))
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)



class OrbitingBody(CelestialBody):
    """
    Considérez cette classe comme abstraite. Planet et Satellite héritent directement de cette classe.\n
    Ce type de corps céleste se base sur une référence (de type Sun ou Planet) autour de laquelle celui-ci orbite pour déterminer sa position.
    """
    def __init__(self, id, color, orbitRef):
        self.angle = 0
        self.orbitCount = 0
        self.orbitReference = orbitRef
        super().__init__(id, color)
        # Distance du soleil : "semimajorAxis"
        # Rayon : "meanRadius"
        # Jours par orbite = "sideralOrbit"
        # Jours par rotation sur soi-même = "sideralRotation" (inutilisé actuellement)
        self.daysPerOrbit = self.apiData["sideralOrbit"]
        self.distanceFromOrbitCenter = self.apiData["semimajorAxis"]*DISTANCE_SCALE
        self.refresh()
    
    def __str__(self):
        s = super().__str__()
        s += "Nombre d'orbites : " + str(self.orbitCount) + "\n"
        s += "Angle : " + str(self.angle) + "\n"
        return s

    def refresh(self):
        self.updatePosition()
        if displayPlanetOrbits:
            self.drawOrbit()
        self.draw()

    def updatePosition(self):
        if(self.daysPerOrbit != 0):
            self.orbitCount += (SPEED_MULTIPLIERS[speedMultiplierIndex]/FRAMERATE)/self.daysPerOrbit
            self.angle = (2*math.pi)*self.orbitCount
            self.x = (self.distanceFromOrbitCenter*math.cos(self.angle))*DISTANCE_SCALE + self.orbitReference.x
            self.y = (self.distanceFromOrbitCenter*math.sin(self.angle))*DISTANCE_SCALE + self.orbitReference.y

    def drawOrbit(self):
        pygame.draw.circle(screen, (255, 255, 255), (self.orbitReference.x, self.orbitReference.y), self.distanceFromOrbitCenter*DISTANCE_SCALE, 1)

class Planet(OrbitingBody):
    def __init__(self, id, color, orbitRef):
        super().__init__(id, color, orbitRef)
        self.radius *= PLANET_SCALE
        self.distanceFromOrbitCenter += PLANET_ORBIT_OFFSET
        # Récupération des satellites
        satelliteInfo = self.apiData["moons"]
        self.satellites = []
        if (satelliteInfo is not None and ENABLE_SATELLITES == True): # Une planète peut ne pas avoir de satellite, comme par exemple Mercure
            for s in satelliteInfo:
                satId = s["rel"].rsplit('/', 1)[-1] # Récupère le dernier mot de l'url pour avoir l'ID du satellite (voir explication dans api.py)
                self.satellites.append(Satellite(satId, SATELLITE_COLOR, self)) 
        self.radius *= PLANET_SCALE

class Satellite(OrbitingBody):
    def __init__(self, id, color, orbitRef):
        super().__init__(id, color, orbitRef)
        self.radius *= SATELLITE_SCALE

class Sun(CelestialBody):
    """
    Corps de référence de la simulation, il est considéré comme immobile.\n
    """
    def __init__(self):
        super().__init__("Sun", SUN_COLOR, SUN_X, SUN_Y)
        self.radius *= SUN_SCALE
        self.planets = []
        for p in PLANETS:
            self.planets.append(Planet(p[0], p[1], self))
        super().draw()


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
    sun.draw()

    clock.tick(FRAMERATE)
    pygame.display.flip()