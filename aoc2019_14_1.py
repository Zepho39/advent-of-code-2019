import logging

logging.basicConfig(filename='aoc2019_14_1.log',level=logging.DEBUG)

# Need/Out * Reduction
def reverseReaction(chem, chemDict):
	cost = 0
	for k, v in chemDict[chem].items():
		if k == 'ORE':
			logging.debug("reverseReaction: chem = {}: key is {} and value is {}".format(chem,k,v))
			cost += v
		if k not in ['OUT', 'ORE']:
			logging.debug("reverseReaction: chem = {}: current cost for chemical {} is {}".format(chem, chem, cost))
			logging.debug("reverseReaction: chem = {}: key = {}, value = {}, chemDict[{}] = {}".format(chem, k, v, k, chemDict[k]))
			cost += (v/chemDict[k]['OUT']) * reverseReaction(k, chemDict)
	return cost

def seedChemDict(file):
	chemDict = {}
	with open(file) as reactions:
		reaction = reactions.readline()
		while reaction:
			args = reaction.replace('\n', '').split(' => ')
			logging.debug("seedChemDict: Reaction after split = {}".format(args))
			out = args[1].split(' ')
			logging.debug("seedChemDict: Right side of reaction after split = {}".format(out))
			inputs = args[0].split(',')
			logging.debug("seedChemDict: Left side of reaction after split = {}".format(inputs))
			chemDict[out[1]] = {}
			chemDict[out[1]]['OUT'] = int(out[0])
			for inp in inputs:
				i = inp.strip().split(' ')
				logging.debug("seedChemDict: Input chemical after split on space = {}".format(i))
				chemDict[out[1]][i[1]] = int(i[0])
			reaction = reactions.readline()
	print(chemDict)
	return chemDict

#seedChemDict('aoc2019_14.test1.txt')
chemDict = seedChemDict('aoc2019_14.test1.txt')
cost = reverseReaction('FUEL', chemDict)
print(cost)