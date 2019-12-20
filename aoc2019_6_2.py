
#PLANET_INPUT_FILE = '/Users/bkelly/Desktop/Advent/2019/aoc2019_6_1_testInput1.txt'
#PLANET_INPUT_FILE = '/Users/bkelly/Desktop/Advent/2019/aoc2019_6_2_testInput2.txt'
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

def countOrbits(planet, endPlanet):
    orbits = 0
    #print(planet.getName())
    if planet.getName() == endPlanet:
        return 0
    else:
        return 1 + countOrbits(planet.getOrbitee(), endPlanet)

def countAllOrbits(listOfPlanets):
    totalOrbits = 0
    for planet in listOfPlanets:
        #print(planet.getName())
        totalOrbits += countOrbits(planet, 'COM')

    return totalOrbits

# Return format should be one of 'dict', 'list'
def seedPlanets(filename, returnFormat='list'):
    dictOfPlanets = {}
    with open(PLANET_INPUT_FILE) as planets:
        planet = planets.readline()
        while planet:
            orbit = planet.rstrip().split(')')
            #print(orbit)
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
    if returnFormat == 'dict':
        return dictOfPlanets
    elif returnFormat == 'list':
        return list(dictOfPlanets.values())
    else:
        print('ERROR: Unsuported return format {} FROM seedPlanets({})'.format(returnFormat, filename))
        return 'Unsuported return format {}'.format(returnFormat)

def findCommonOrbitees(planet1, planet2):
    orbitees1 = findOrbitees(planet1)
    orbitees2 = findOrbitees(planet2)
    #print(orbitees1)
    #print(orbitees2)
    return set(orbitees1).intersection(orbitees2)

# Returns the list of all parents up through COM
def findOrbitees(planet):
    orbitees = []
    p = planet
    orbitee = ''
    while orbitee not in ['COM', False]:
        #print(p.getName())
        p = p.getOrbitee()
        orbitees.append(p.getName())
        orbitee = p.getName()
    return orbitees

def findShortestPath(planet1, planet2):
    commonOrbitees = findCommonOrbitees(planet1, planet2)
    shortestTransfer = -1
    for p in commonOrbitees:
        #print(p.getName())
        path1 = countOrbits(planet1, p)
        path2 = countOrbits(planet2, p)
        if path1 + path2 < shortestTransfer or shortestTransfer < 0:
            shortestTransfer = path1 + path2
    return shortestTransfer

def aoc2019_6_1():
    listOfPlanets = seedPlanets(PLANET_INPUT_FILE)
    #print(listOfPlanets)
    print("Total Orbits = {}".format(countAllOrbits(listOfPlanets)))


def aoc2019_6_2():
    listOfPlanets = seedPlanets(PLANET_INPUT_FILE, 'dict')
    print("Shortest Transfer Path = {}".format(findShortestPath(listOfPlanets['YOU'], listOfPlanets['SAN']) - 2))


#aoc2019_6_1()
aoc2019_6_2()









