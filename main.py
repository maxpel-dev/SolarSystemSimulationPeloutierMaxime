import api
import pygame
import math

pygame.init()
# Vous pouvez ajuster la résolution selon la taille de votre écran (Adapté à un écran 15 pouces par défaut)
w,h = 1520, 768
FRAMERATE = 165 # Fréquence (en Hz) de rafraîchissement de l'affichage, n'affecte pas la vitesse de la simulation
screen = pygame.display.set_mode((w,h))

# Vitesse de la simulation - Régler avec ↑ (ou 'Z') et ↓ (ou 'S')
SPEED_MULTIPLIERS = [0.1, 0.2, 0.3, 0.5, 1, 2, 5, 10, 50, 100, 250, 500, 1000, 5000, 10000]
speedMultiplierIndex = 6 # Indice de la vitesse initiale
displayPlanetOrbits = True # On/Off avec la touche 'E'
displaySatelliteOrbits = False # On/off avec la touche 'R'
# Vue 1 (par défaut) : Proportion réduite du soleil pour voir l'orbite complète des planètes qui en sont proches
# Vue 2 : Même échelle pour le soleil et les planètes
# Vue 3 : Soleil centré à échelle grandement réduite, seules les planètes proches de celui-ci seront visibles
VIEW = 1 # Changez cette valeur pour choisir le numéro de la vue
# Vous pouvez augmenter la valeur de cette constante pour afficher plus de satellites au prix d'un chargement initial plus long.
# Vous pouvez également la diminuer jusqu'à 0. 
# Au-delà des 5 premiers, les satellites éloignés des génates gazeuses ont des orbites très grandes et ne rendent pas très bien avec les échelles choisies.
MAX_SATELLITES_PER_PLANET = 5
# Echelles - Vous pouvez vous amuser à jouer avec, je pense avoir trouvé un bon équilibre entre précision et lisibilité d'affichage.
# C'est loin d'être réaliste, mais l'objectif c'est que ça aie l'air cool.
# Selon le numéro de vue choisie, certaines de ces valeurs peuvent être surchargées.
PLANET_SCALE = 1/1000
SATELLITE_SCALE = 1/500
PLANET_DISTANCE_SCALE = 1/1600
SATELLITE_DISTANCE_SCALE = 200/MAX_SATELLITES_PER_PLANET
# Cette constante est utilisée pour s'assurer que les satellites soient suffisamment espacés dans l'affichage.
ADDED_SPACE_BETWEEN_SATELLITES = (1/SATELLITE_SCALE)*4

match VIEW:
    case 1:
        SUN_X, SUN_Y = 220, h/2
        SUN_SCALE = 1/5500
    case 2:
        SUN_X, SUN_Y = -450, h/2
        SUN_SCALE = 1/1000
    case 3:
        SUN_X, SUN_Y = w/2, h/2
        SUN_SCALE = 1/7000
        PLANET_SCALE = 1/400
        SATELLITE_SCALE = PLANET_SCALE
        PLANET_DISTANCE_SCALE = 1/800
    case other:
        SUN_X, SUN_Y = 220, h/2
        SUN_SCALE = 1/5500
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
SUN_COLOR = (235, 158, 26)
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
        # Distance du centre de l'orbite : "semimajorAxis"
        # Rayon : "meanRadius"
        # Jours par orbite = "sideralOrbit"
        # Jours par rotation sur soi-même = "sideralRotation" (inutilisé actuellement)
        self.daysPerOrbit = self.apiData["sideralOrbit"]
        self.distanceFromOrbitCenter = (self.apiData["semimajorAxis"] + self.orbitReference.radius)*PLANET_DISTANCE_SCALE
    
    def __str__(self):
        s = super().__str__()
        s += "Nombre d'orbites : " + str(self.orbitCount) + "\n"
        s += "Angle : " + str(self.angle) + "\n"
        return s

    def refresh(self):
        self.updatePosition()
        if ((issubclass(type(self), Planet) and displayPlanetOrbits)
        or (issubclass(type(self), Satellite) and displaySatelliteOrbits)):
            self.drawOrbit()
        super().draw()

    def updatePosition(self):
        if(self.daysPerOrbit != 0):
            self.orbitCount += (SPEED_MULTIPLIERS[speedMultiplierIndex]/FRAMERATE)/self.daysPerOrbit
            self.angle = (2*math.pi)*self.orbitCount
            self.x = (self.distanceFromOrbitCenter*math.cos(self.angle))*PLANET_DISTANCE_SCALE + self.orbitReference.x
            self.y = (self.distanceFromOrbitCenter*math.sin(self.angle))*PLANET_DISTANCE_SCALE + self.orbitReference.y

    def drawOrbit(self):
        pygame.draw.circle(screen, (255, 255, 255), (self.orbitReference.x, self.orbitReference.y), self.distanceFromOrbitCenter*PLANET_DISTANCE_SCALE, 1)

class Planet(OrbitingBody):
    """
    Planète orbitant autour du soleil.
    """
    def __init__(self, id, color, orbitRef):
        super().__init__(id, color, orbitRef)
        self.radius *= PLANET_SCALE
        self.distanceFromOrbitCenter += self.orbitReference.radius/PLANET_DISTANCE_SCALE
        self.refresh()
        # Récupération des satellites
        self.satellites = []
        satelliteInfo = self.apiData["moons"]
        if (satelliteInfo is not None): # Une planète peut ne pas avoir de satellite, comme par exemple Mercure
            for i, s in enumerate(satelliteInfo):
                if(i >= MAX_SATELLITES_PER_PLANET):
                    break
                satId = s["rel"].rsplit('/', 1)[-1] # Récupère le dernier mot de l'url pour avoir l'ID du satellite (voir explication dans api.py)
                self.satellites.append(Satellite(satId, SATELLITE_COLOR, self)) 

class Satellite(OrbitingBody):
    """
    Satellite naturel (ou "lune") d'une planète orbitant autour de celle-ci.
    """
    def __init__(self, id, color, orbitRef):
        super().__init__(id, color, orbitRef)
        self.radius *= SATELLITE_SCALE
        if (self.radius <= 1):
            self.radius = 1
        self.distanceFromOrbitCenter *= SATELLITE_DISTANCE_SCALE
        self.distanceFromOrbitCenter += self.orbitReference.radius/PLANET_DISTANCE_SCALE
        # Assure un éloignement minimum entre la planète et les satellites ainsi qu'entre les satellites eux-mêmes.
        self.distanceFromOrbitCenter += (len(self.orbitReference.satellites)+2)*ADDED_SPACE_BETWEEN_SATELLITES
        # print("Distance du centre de l'orbite de " + self.id + " : " +  str(self.distanceFromOrbitCenter))

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
        if event.type == pygame.KEYUP:
            print(event.unicode)
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
            if event.key == pygame.K_e:
                displayPlanetOrbits = not displayPlanetOrbits
            if event.key == pygame.K_r:
                displaySatelliteOrbits = not displaySatelliteOrbits


    # Rafraîchissement de l'affichage du système solaire
    screen.fill((0,0,0))
    sun.draw()
    for planet in sun.planets:
        planet.refresh()
        for satellite in planet.satellites:
            satellite.refresh()


    clock.tick(FRAMERATE)
    pygame.display.flip()