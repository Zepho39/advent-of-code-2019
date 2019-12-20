


PLANET_INPUT_FILE = '/Users/bkelly/Desktop/Advent/2019/aoc2019_6_1_input.txt'

class Planet:
    def __init__(self, name):
        # List of Planets directly orbiting this one
        self.orbiters = []
        self.orbitee = False
        self.name = name

    # Adds another planet to the list of orbiters
    def addOrbiter(self, planet):
        self.orbiters.append(planet)
        planet.setOrbitee(self)

    def setOrbitee(self, planet):
        self.orbitee = planet

    # parent
    def getOrbitee(self):
        return self.orbitee 

    # children
    def getOrbiters(self):
        return self.orbiters 

    def getName(self):
        return self.name

def countOrbits(planet):
    orbits = 0
    #print(planet.getName())
    if planet.getName() == 'COM':
        return 0
    else:
        return 1 + countOrbits(planet.getOrbitee())

def countAllOrbits(listOfPlanets):
    totalOrbits = 0
    for planet in listOfPlanets:
        print(planet.getName())
        totalOrbits += countOrbits(planet)

    return totalOrbits

def seedPlanets(filename):
    dictOfPlanets = {}
    with open(PLANET_INPUT_FILE) as planets:
        planet = planets.readline()
        while planet:
            orbit = planet.rstrip().split(')')
            print(orbit)
            orbitee = orbit[0]
            #print(orbitee)
            orbiter = orbit[1]
            #print(orbiter)
            currOrbitee = dictOfPlanets.get(orbitee, Planet(orbitee))
            #print(currOrbitee)
            currOrbiter = dictOfPlanets.get(orbiter, Planet(orbiter))
            #print(currOrbiter)
            currOrbiter.setOrbitee(currOrbitee)
            currOrbitee.addOrbiter(currOrbiter)
            #print(currOrbitee)
            currOrbiter.setOrbitee(currOrbitee)
            dictOfPlanets[orbitee] = currOrbitee
            dictOfPlanets[orbiter] = currOrbiter
            planet = planets.readline()
    return list(dictOfPlanets.values())


def aoc2019_6_1():
    listOfPlanets = seedPlanets(PLANET_INPUT_FILE)
    #print(listOfPlanets)
    print("Total Orbits = {}".format(countAllOrbits(listOfPlanets)))

aoc2019_6_1()