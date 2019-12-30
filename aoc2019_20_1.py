

INPUT = ''

def buildDonut(file):
	donut = {}
	portals = {}
	portalPieces = {}
	donutGraph = {}
	y = 0
	width = 0
	start = (0, 0)
	end = (0, 0)
	with open(file) as donutMap:
		donutLine = donutMap.readline().strip('\n')
		width = len(donutLine)
		while donutLine:
			for x in range(width):
				donut[(x, y)] = donutLine[x]
			y += 1
			donutLine = donutMap.readline().strip('\n')
	#print(donut)
	for why in range(y):
		for x in range(width):
			if donut[(x, why)].isupper():
				if donut.get((x+1, why), '?').isupper() and donut.get((x+2, why), '?') == '.':
					portal = portals.get(donut.get((x, why), '?') + donut[(x+1, why)], [])
					portal.append((x+2, why))
					print("Portal {} = {}".format(donut.get((x, why), '?') + donut[(x+1, why)], portal))
					portals[donut[(x, why)] + donut[(x+1, why)]] = portal
				elif donut.get((x-1, why), '?') == '.' and donut.get((x+1, why), '?').isupper():
					portal = portals.get(donut[(x, why)] + donut.get((x+1, why), '?'), [])
					portal.append((x-1, why))
					print("Portal {} = {}".format(donut.get((x, why), '?') + donut[(x+1, why)], portal))
					portals[donut[(x, why)] + donut[(x+1, why)]] = portal
				elif donut.get((x, why+1), '?').isupper() and donut.get((x, why+2), '?') == '.':
					portal = portals.get(donut[(x, why)] + donut[(x, why+1)], [])
					portal.append((x, why+2))
					print("Portal {} = {}".format(donut.get((x, why), '?') + donut[(x, why+1)], portal))
					portals[donut[(x, why)] + donut[(x, why+1)]] = portal
				elif donut.get((x, why+1), '?').isupper() and donut.get((x, why-1), '?') == '.':
					portal = portals.get(donut[(x, why)] + donut[(x, why+1)], [])
					portal.append((x, why-1))
					print("Portal {} = {}".format(donut.get((x, why), '?') + donut[(x, why+1)], portal))
					portals[donut[(x, why)] + donut[(x, why+1)]] = portal
			elif donut[(x, why)] == '.':
				if donut.get((x-1, why), '?') == '.':
					don = donutGraph.get((x, why), [])
					don.append((x-1, why))
					donutGraph[(x, why)] = don 
				if donut.get((x+1, why), '?') == '.':
					don = donutGraph.get((x, why), [])
					don.append((x+1, why))
					donutGraph[(x, why)] = don
				if donut.get((x, why-1), '?') == '.':
					don = donutGraph.get((x, why), [])
					don.append((x, why-1))
					donutGraph[(x, why)] = don
				if donut.get((x, why+1), '?') == '.':
					don = donutGraph.get((x, why), [])
					don.append((x, why+1))
					donutGraph[(x, why)] = don
	# k should be the portal name, v should be a tuple of the two points of the portal
	print(portals)
	for k, v in portals.items():
		if k == 'AA':
			start = v[0]
		elif k == 'ZZ':
			end = v[0]
		else:
			print("Key = {} and Value = {}".format(k, v))
			donutGraph[v[0]].append(v[1])
			donutGraph[v[1]].append(v[0])
	print(donutGraph)
	return (donutGraph, width, y, start, end)

def djikstraPath(start, end, graph):
    # shortest paths is a dict of nodes
    # whose value is a tuple of (previous node, weight)
    shortest_paths = {start: (None, 0)}
    current_node = start
    visited = set()
    
    while current_node != end:
        visited.add(current_node)
        destinations = graph[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            weight = 1 + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)
        
        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not next_destinations:
            return "Route Not Possible"
        # next node is the destination with the lowest weight
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])
    
    # Work back through destinations in shortest path
    path = []
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node
    # Reverse path
    path = path[::-1]
    return path

graph = buildDonut('aoc2019_20.input.txt')
djikstra = djikstraPath(graph[3], graph[4], graph[0])
print(djikstra)
print(len(djikstra)-1)



