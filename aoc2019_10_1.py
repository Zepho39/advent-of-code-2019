import logging
from fractions import Fraction

INPUT_PATH = 'aoc2019_10_1.input.txt'

def init():

	logging.basicConfig(filename='aoc2019_10_1.log',level=logging.INFO)

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
print(getMaxAsteroidSight(INPUT_PATH))