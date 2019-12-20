

MIN = 240920
MAX = 789857


def passConsDups(num):
	startInd = 0
	nString = str(num)
	grps = {}

	for i in range(len(nString)):
		if (i + 1) == len(nString):
			continue
		if nString[i] == nString[i+1]:
			grps[startInd] = grps.get(startInd, 0) + 1
			if i == 0:
				grps[startInd] = grps.get(startInd, 0) + 1
		elif nString[i] != nString[i+1]:
			startInd = i
			grps[startInd] = grps.get(startInd, 0) + 1
	print(grps)
	return 2 in grps.values()

def passIncreasing(num):
	nString = str(num)
	for i in range(len(nString)):
		if (i + 1) == len(nString):
			return True
		if int(nString[i]) > int(nString[i+1]):
			return False
	return True


def passAllChecks(num):
	return (passIncreasing(num) and passConsDups(num))


def passwordsInRange():
	global MIN
	global MAX
	passwords = []
	for i in range(MIN, MAX + 1):
		if passAllChecks(i):
			passwords.append(i)
	return passwords

print(len(passwordsInRange()))

#print(passAllChecks(112222222))