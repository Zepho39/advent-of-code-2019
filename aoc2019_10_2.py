import logging
from fractions import Fraction
import math

INPUT_PATH = 'aoc2019_10_1.input.txt'

def init():
	logging.basicConfig(filename='aoc2019_10_2.log',level=logging.DEBUG)

def createAsteroidBeltArray(file):
	logging.debug("createAsteroidBeltArray starting, file = {}".format(file))
	row = 0
	asteroidBelt = []
	with open(file) as asteroids:
		asteroidRow = asteroids.readline()
		while asteroidRow:
			asteroidBelt.append([])
			for i in range(0, len(asteroidRow.replace('\n', ''))):
				logging.debug("createAsteroidBeltArray row = {} index = {} value = {}".format(row, i, asteroidRow[i]))
				asteroidBelt[row].append(asteroidRow[i])
			asteroidRow = asteroids.readline()
			row += 1
	return asteroidBelt

# Assumes input is an array of arrays of chars
def getAsteroidCoords(asteroidArray):
	asteroidCoords = []
	for idx, asteroidRow in enumerate(asteroidArray):
		for i in range(0, len(asteroidRow)):
			if asteroidRow[i] == '#':
				asteroidCoords.append((i, idx))
	return asteroidCoords 

# Function makes the assumption that coord1 != coord2
def drawLine(coord1, coord2, beltHeight, beltWidth):
	vector = []
	xInit = coord1[0]
	yInit = coord1[1]
	xInc = 0
	yInc = 0
	if coord2[0] - coord1[0] == 0:
		xInc = 0
		yInc = 1 if coord2[1] - coord1[1] > 0 else -1
		yIntCompare = 0 if (yInc > 1) else -1
		while yInit < beltHeight and yInit > yIntCompare:
			logging.debug("drawLine xInc = {}, yInc = {}, xInit = {}, yInit = {}, coord1 = {}, coord2 = {}, beltHeight = {}, beltWidth = {}".format(xInc, yInc, xInit, yInit, coord1, coord2, beltHeight, beltWidth))
			vector.append((xInit, yInit))
			xInit += xInc
			yInit += yInc
		logging.debug("drawLine xInc = {}, yInc = {}, xInit = {}, yInit = {}, coord1 = {}, coord2 = {}, beltHeight = {}, beltWidth = {}".format(xInc, yInc, xInit, yInit, coord1, coord2, beltHeight, beltWidth))
		vector.append((xInit, yInit))
		xInit += xInc
		yInit += yInc
	elif coord2[1] - coord1[1] == 0:
		xInc = 1 if coord2[0] - coord1[0] > 0 else -1
		yInc = 0
		xIntCompare = 0 if (xInc > 1) else -1
		while xInit < beltWidth and xInit > xIntCompare:
			logging.debug("drawLine xInc = {}, yInc = {}, xInit = {}, yInit = {}, coord1 = {}, coord2 = {}, beltHeight = {}, beltWidth = {}".format(xInc, yInc, xInit, yInit, coord1, coord2, beltHeight, beltWidth))
			vector.append((xInit, yInit))
			xInit += xInc
			yInit += yInc
		logging.debug("drawLine xInc = {}, yInc = {}, xInit = {}, yInit = {}, coord1 = {}, coord2 = {}, beltHeight = {}, beltWidth = {}".format(xInc, yInc, xInit, yInit, coord1, coord2, beltHeight, beltWidth))
		vector.append((xInit, yInit))
		xInit += xInc
		yInit += yInc
	else: 
		# (1, 0), (3, 1)   coord1 = (1, 0), coord2 = (2, 3), beltHeight = 20, beltWidth = 20
		frac = abs(Fraction((coord2[0] - coord1[0]) , (coord2[1] - coord1[1])))
		logging.debug("drawLine: slope = {}".format(frac))
		xInc = frac.numerator if coord2[0] - coord1[0] > 0 else -1 * frac.numerator
		yInc = frac.denominator if coord2[1] - coord1[1] > 0 else -1 * frac.denominator
		while xInit < beltWidth and yInit < beltHeight and (xInit > 0 or coord1[0] == 0) and (yInit > 0 or coord1[1] == 0):
			logging.debug("drawLine xInc = {}, yInc = {}, xInit = {}, yInit = {}, coord1 = {}, coord2 = {}, beltHeight = {}, beltWidth = {}".format(xInc, yInc, xInit, yInit, coord1, coord2, beltHeight, beltWidth))
			vector.append((xInit, yInit))
			xInit += xInc
			yInit += yInc
		logging.debug("drawLine xInc = {}, yInc = {}, xInit = {}, yInit = {}, coord1 = {}, coord2 = {}, beltHeight = {}, beltWidth = {}".format(xInc, yInc, xInit, yInit, coord1, coord2, beltHeight, beltWidth))
		vector.append((xInit, yInit))
		xInit += xInc
		yInit += yInc

	return vector

def sortByProximity(asteroid, listOfAsteroids): 
	listOfAsteroids.sort(key = lambda coord: math.sqrt((coord[0] - asteroid[0])**2 + (coord[1] - asteroid[1])**2))  
	return listOfAsteroids

# Returns a dictionary of sections of the map, where each list of coord tuples is sorted ascending by proximity to start coord
def buildResearchStation(asteroid, otherAsteroids):
	sections = {1:[], 2:{}, 3:[], 4:{}, 5:[], 6:{}, 7:[], 8:{}}
	logging.debug("buildResearchStation sections initialized to {}".format(sections))
	for a in otherAsteroids:
		# Section 1
		if a[0] - asteroid[0] == 0 and a[1] - asteroid[1] < 0:
			logging.debug("buildResearchStation adding {} to section 1".format(a))
			sections[1].append(a)
		# Section 2
		elif a[0] - asteroid[0] > 0 and a[1] - asteroid[1] < 0:
			slope = (a[1] - asteroid[1]) / (a[0] - asteroid[0])
			logging.debug("buildResearchStation adding {} to section 2 at slope {}".format(a, slope))
			newSlope = sections[2].get(slope, [])
			newSlope.append(a)
			logging.debug("buildResearchStation new array for this slope = {}".format(newSlope))
			sections[2][slope] = newSlope
			logging.debug("buildResearchStation section 2 now set to {}".format(sections[2]))
		# Section 3
		elif a[0] - asteroid[0] > 0 and a[1] - asteroid[1] == 0:
			logging.debug("buildResearchStation adding {} to section 3".format(a))
			sections[3].append(a)
		# Section 4
		elif a[0] - asteroid[0] > 0 and a[1] - asteroid[1] > 0:
			slope = (a[1] - asteroid[1]) / (a[0] - asteroid[0])
			logging.debug("buildResearchStation adding {} to section 4 at slope {}".format(a, slope))
			newSlope = sections[4].get(slope, [])
			newSlope.append(a)
			logging.debug("buildResearchStation new array for this slope = {}".format(newSlope))
			sections[4][slope] = newSlope
			logging.debug("buildResearchStation section 4 now set to {}".format(sections[4]))
		# Section 5
		elif a[0] - asteroid[0] == 0 and a[1] - asteroid[1] > 0:
			logging.debug("buildResearchStation adding {} to section 5".format(a))
			sections[5].append(a)
		# Section 6
		elif a[0] - asteroid[0] < 0 and a[1] - asteroid[1] > 0:
			slope = (a[1] - asteroid[1]) / (a[0] - asteroid[0])
			logging.debug("buildResearchStation adding {} to section 6 at slope {}".format(a, slope))
			newSlope = sections[6].get(slope, [])
			newSlope.append(a)
			logging.debug("buildResearchStation new array for this slope = {}".format(newSlope))
			sections[6][slope] = newSlope
			logging.debug("buildResearchStation section 6 now set to {}".format(sections[6]))
		# Section 7
		elif a[0] - asteroid[0] < 0 and a[1] - asteroid[1] == 0:
			logging.debug("buildResearchStation adding {} to section 7".format(a))
			sections[7].append(a)
		# Section 8
		elif a[0] - asteroid[0] < 0 and a[1] - asteroid[1] < 0:
			slope = (a[1] - asteroid[1]) / (a[0] - asteroid[0])
			logging.debug("buildResearchStation adding {} to section 8 at slope {}".format(a, slope))
			newSlope = sections[8].get(slope, [])
			newSlope.append(a)
			logging.debug("buildResearchStation new array for this slope = {}".format(newSlope))
			sections[8][slope] = newSlope
			logging.debug("buildResearchStation section 8 now set to {}".format(sections[8]))
	logging.debug("buildResearchStation finished adding coordinates to sections")
	for item in sections.items():
		logging.debug("buildResearchStation item = {}".format(item))
		key = item[0]
		value = item[1]
		if key in [1,3,5,7]:
			sections[key] = sortByProximity(asteroid, value)
		elif key in [2,4,6,8]:
			for item in sections[key].items():
				slope = item[0]
				asts = item[1]
				sections[key][slope] = sortByProximity(asteroid, asts)
	logging.debug("buildResearchStation finished sorting sections")
	return sections


def vaporize(file, asteroid):
	logging.debug("vaporize starting")
	asteroidBelt = createAsteroidBeltArray(file)
	asteroidCoords = getAsteroidCoords(asteroidBelt)
	beltHeight = len(asteroidBelt)
	beltWidth = len(asteroidBelt[0])
	logging.debug("vaporize asteroidBelt = {}".format(asteroidBelt))
	logging.debug("vaporize asteroidCoords = {}".format(asteroidCoords))
	logging.debug("vaporize started")
	sections = buildResearchStation(asteroid, asteroidCoords)
	step = 0
	sec = 1
	ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])
	secFinished = [False, False, False, False, False, False, False, False]
	while (step < 200) and (False in secFinished):
		if sec in [1, 3, 5, 7]:
			if not secFinished[sec-1]:
				print("The {} asteroid to be vaporized is at {}.".format(ordinal(step+1), sections[sec].pop(0)))
				step += 1
			if len(sections[sec]) == 0:
				secFinished[sec-1] = True
			sec += 1
		elif sec in [2, 4, 6, 8]:
			if not secFinished[sec-1]:
				secFinCounter = True
				for key in sorted(sections[sec]):
					if len(sections[sec][key]) != 0:
						print("The {} asteroid to be vaporized is at {}.".format(ordinal(step+1), sections[sec][key].pop(0)))
						step += 1
						if len(sections[sec][key]) != 0:
							secFinCounter = False
				secFinished[sec-1] = secFinCounter
			if sec == 8:
				sec = 1
			else:
				sec += 1



def getMaxAsteroidSight(file):
	logging.debug("getMaxAsteroidSight starting")
	asteroidBelt = createAsteroidBeltArray(file)
	asteroidCoords = getAsteroidCoords(asteroidBelt)
	beltHeight = len(asteroidBelt)
	beltWidth = len(asteroidBelt[0])
	maxOtherAsteroids = 0
	maxOtherAsteroidsCoord = (-1 , -1)
	logging.debug("getMaxAsteroidSight asteroidBelt = {}".format(asteroidBelt))
	logging.debug("getMaxAsteroidSight asteroidCoords = {}".format(asteroidCoords))
	logging.debug("getMaxAsteroidSight started")
	seenAsteroids = {}
	for asteroid in asteroidCoords:
		seenAsteroids[asteroid] = []
		lines = []
		logging.debug("getMaxAsteroidSight asteroid = {}".format(asteroid))
		for a in asteroidCoords:
			logging.debug("getMaxAsteroidSight compare asteroid {}".format(a))
			if a != asteroid:
				logging.debug("getMaxAsteroidSight lines before comparing {} to {} is {}".format(asteroid, a, lines))
				inLines = False
				for line in lines:
					if a in line:
						logging.debug("getMaxAsteroidSight: asteroid {} already in line {}".format(a, line))
						inLines = True
				if not inLines:
					lines.append(drawLine(asteroid, a, beltHeight, beltWidth))
					logging.info("getMaxAsteroidSight: asteroid {} can see {}".format(asteroid, a))
					seenAsteroids[asteroid].append(a)

				logging.debug("getMaxAsteroidSight lines after comparing {} to {} is {}".format(asteroid, a, lines))

		logging.debug("getMaxAsteroidSight current maxOtherAsteroids = {} for coord {}".format(maxOtherAsteroids, maxOtherAsteroidsCoord))
		logging.debug("getMaxAsteroidSight asteroid {} can see {} others".format(asteroid, len(lines)))
		logging.debug("getMaxAsteroidSight asteroid {} can see {}".format(asteroid, seenAsteroids.get(asteroid, "NONE")))

		if len(lines) > maxOtherAsteroids:
			maxOtherAsteroids = len(lines)
			maxOtherAsteroidsCoord = asteroid
	logging.info("getMaxAsteroidSight: coord of max asteroids = {}, max asteroids = {}".format(maxOtherAsteroidsCoord, maxOtherAsteroids))
	print("getMaxAsteroidSight: coord of max asteroids = {}, max asteroids = {}".format(maxOtherAsteroidsCoord, maxOtherAsteroids))
	return maxOtherAsteroids

init()
print(vaporize(INPUT_PATH, (17, 22)))

#The 200th asteroid to be vaporized is at (6, 16).
