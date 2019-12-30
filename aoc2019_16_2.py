import numpy
import math

BASE_PATTERN = [0, 1, 0, -1]
TEST_SIGNAL1 = '12345678'
TEST_SIGNAL2 = '48226158'
TEST_SIGNAL3 = '80871224585914546619083218645595'
TEST_SIGNAL4 = '19617804207202209144916044189917'
TEST_SIGNAL5 = '69317163492948606335995924319873'
TEST_SIGNAL6 = '03036732577212944063491565474664'
TEST_SIGNAL7 = '02935109699940807407585447034323'
TEST_SIGNAL8 = '03081770884921959731165446850517'
INPUT_SIGNAL = '59777098810822000809394624382157501556909810502346287077282177428724322323272236375412105805609092414782740710425184516236183547622345203164275191671720865872461284041797089470080366457723972985763645873208418782378044815481530554798953528896905275975178449123276858904407462285078456817038667669183420974001025093760473977009037844415364079145612611938513254763581971458140349825585640285658557835032882311363817855746737733934576748280568150394709654438729776867932430014255649458605325527757230466997043406136400716198065838842158274093116050506775489075879316061475634889155814030818530064869767243196343272137745926937355015378474209347100518533'

# Consumes a positive integer, returns an array of integers making up each digit of the input integer
def signalToArray(signal):
	return [(signal//(10**i))%10 for i in range(math.ceil(math.log(signal, 10))-1, -1, -1)]

#def phasePattern(phase):

def chunkSignal(signal, chunkSize):
	chunks = []
	for i in range(0, len(signal), chunkSize):
		chunks.append(signal[i:i + chunkSize])
	return chunks

# Returns nth digit of number, counting right to left
def get_digit(number, n):
    return number // 10**n % 10

def calculateSubPhase(signal, subPhase):
	sigArray = signal.copy()
	#patternArray = []
	#for p in range(0, subPhase+1):
	sigArray.insert(0, 0)
		#patternArray.append(BASE_PATTERN)
	#sigArray += signalToArray(signal)
	signalChunks = chunkSignal(sigArray, subPhase+1)
	fftElement = 0
	for i in range(0, len(signalChunks)):
		arr = list(map(lambda sig : sig * BASE_PATTERN[i % len(BASE_PATTERN)], signalChunks[i]))
		#print("DEBUG: calculateSubPhase: chunk = {}, mapped array = {}".format(signalChunks[i], arr))
		sumArr = numpy.sum(arr)
		#print("DEBUG: calculateSubPhase: fftElement currently {} and newly calculated chunk = {}".format(fftElement, sumArr))
		fftElement += sumArr
	return fftElement

# Consumes positive integer, returns positive integer
def calculatePhase(signal):
	#sigArray = signalToArray(signal)
	sigArray = list(map(lambda x: int(x), list(signal)))
	output = ''
	for i in range(0, len(sigArray)):
		out = str(get_digit(abs(calculateSubPhase(sigArray, i)), 0))
		#print("DEBUG: calculatePhase: element for subPhase {} of input {} calculated as {}".format(i, signal, out))
		output += out
	return output

def calculatePhases(signal, phases):
	p = 0
	while p < phases:
		phaseOut = calculatePhase(signal)
		p += 1
		print("INFO: calculatePhases: after {} phases output = {}".format(p, phaseOut))
		signal = phaseOut
	return phaseOut

def createTrueInput(signal, repeat):
	trueSignal = ''
	for r in range(0, repeat):
		trueSignal += signal
	return trueSignal

#print(calculatePhase(TEST_SIGNAL2))
sig = TEST_SIGNAL7
finalSignal = calculatePhases(createTrueInput(sig, 2), 106)
print("Final Signal = {}".format(finalSignal))
print("Output Code = {}".format(finalSignal[int(sig[:7]):int(sig[:7])+8]))





