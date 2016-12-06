import sys
import random
from operator import itemgetter
import heapq


'''
For the part 1, I have created some function to help finding shortest
driving distance using best-first search, breadthfirst search, depthfirst search.

openFile(fileName) :-
takes filename, refine the contents and return as a list

processCityMap(fileCity, dataMap) :-
takes two parameter 'fileCity', 'dataMap'
map all the data key as dictionary and store all the data that is connected to the key

getNeighbor(city, cityMap) :-
takes city and cityMap which is dataMap created from function 'processCityMap',
and returns all the connected points of city

depthFirst(beginningCity, goalCity, cityMap) :-
takes beginningCity, goalCity, cityMap
and returns the path traveled using depthfirst algorithm which uses stack data structure.

breadthFirst(beginningCity, goalCity, cityMap) :-
takes beginningCity, goalCity, cityMap
and returns the path traveled using breadthfirst algorithm by using queue data structure.

best(beginningCity, goalCity, cityMap) :-
best-first search algorithm that takes beginningCity, goalCity, cityMap
and returns the shortest path traveled by using priorityqueue. This is similar to breadthfirst search but
this returns shorter and more optimized shortest path traveled since all the path are enqueued with priority.


As desinging the code for the part 1, we realized these helper function would be useful because as we search through
the data, we would need to know all the possible path to destination at certain city.
Working along, dfs, bfs, best-first all required to check whether the current city has been visited by previous search,
and visited set could not be the result when reaching destination, it was necessary to traceback the parent node of the city but it was not easy as it seemed.
So, we came up with an idea where we push(for stack) and enqueue(for queue) the current city as well as the path traveled so far together to keep track of the path all times.
After reaching destination, then it would be easy to return the path traveled without tracing back to the root.

We have tried all the search methods, dfs, bfs, and best-first and realized that dfs and bfs was not as effiecient as best-first search.
Although breadthfirst was even better than depthfirst, since breadthfirst does not prioritize the enqueued value, it took longer distance to reach the destination.
Best-first search algorithm seemed best among these three search methods because similar to breadthfirst search, we can actually decide which path to take before it goes into much deeper.
Whereas depthfirst search starts from the most deepest node. Therefore we prefer to use the best-first search, then breadthfirst search and lastly depthfirst search.


'''




class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def insert(self, item, priority):
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1

    def remove(self):
        return heapq.heappop(self._queue)[-1]

    def is_empty(self):
        return len(self._queue) == 0


# Open a file given a file name and returns the file pointer
def openFile(fileName):
    try:
        f = open(fileName, "r")
        file_list = f.read().strip().splitlines()
    except IOError:
        print "File", fileName, "cannot be read"
        sys.exit()
    return file_list


# Process all data from the city data file and put them in a dictionary
def processCityMap(fileCity, dataMap):
    for line in fileCity:
        tokens = line.split(" ")
        if len(tokens) != 4:
            print "Error in line:", line
            print "Every line must be: city1 city2 distance route"
            sys.exit()

        city1 = tokens[0]
        city2 = tokens[1]
        distance = int(tokens[2])
        route = tokens[3]

        if dataMap.has_key(city1):
            dataMap[city1].append((city2, distance, route))
        else:
            dataMap[city1] = [(city2, distance, route)]
        if dataMap.has_key(city2):
            dataMap[city2].append((city1, distance, route))
        else:
            dataMap[city2] = [(city1, distance, route)]

# get all the neighbors connected to the city
def getNeighbor(city, cityMap):
    if cityMap.has_key(city) == False:
        print "Error: city", city, "does not exist in the graph."
    else:
        return cityMap[city]


def depthFirst(beginningCity, goalCity, cityMap):
    visited = set()
    stack = list()
    # append currentcity and the path, and acuumulate the path as traveling along.
    stack.append([(beginningCity, 0), [[beginningCity, 0]]])
    while stack:
        currentCity = stack.pop()
        neighbors = getNeighbor(currentCity[0][0], cityMap)
        visited.add(currentCity[0][0])
        if neighbors:
            for neighbor in neighbors:
                if neighbor[0] == goalCity:
                    path = currentCity[1] + [list(neighbor)]
                    total_cost = 0
                    total_seg = 0
                    for i in range(1, len(path)):
                        total_seg += 1
                        total_cost = total_cost + path[i][1]
                        print "- Take " + path[i][2] + " for " + str(path[i][1]) + " miles to " + path[i][0]
                    print "Total road segments: " + str(total_seg)
                    print "Total distance: " + str(total_cost) + "miles"
                    return currentCity[1] + [list(neighbor)]
                if neighbor[0] not in visited:
                    stack.append([neighbor, currentCity[1] + [list(neighbor)]])
    return "Path not found"


def breadthFirst(beginningCity, goalCity, cityMap):
    visited = set()
    queue = list()
    # append currentcity and the path, and acuumulate the path as traveling along.
    queue.append([(beginningCity, 0), [[beginningCity, 0]]])
    while queue:
        currentCity = queue[0]
        queue = queue[1:]
        neighbors = getNeighbor(currentCity[0][0], cityMap)
        visited.add(currentCity[0][0])
        if neighbors:
            for neighbor in neighbors:
                if neighbor[0] == goalCity:
                    path = currentCity[1] + [list(neighbor)]
                    total_cost = 0
                    total_seg = 0
                    for i in range(1, len(path)):
                        total_seg += 1
                        total_cost = total_cost + path[i][1]
                        print "- Take " + path[i][2] + " for " + str(path[i][1]) + " miles to " + path[i][0]
                    print "Total road segments: " + str(total_seg)
                    print "Total distance: " + str(total_cost) + "miles"
                    return currentCity[1] + [list(neighbor)]
                if neighbor[0] not in visited:
                    queue.append([neighbor, currentCity[1] + [list(neighbor)]])

    return "Path not found"


def best(beginningCity, goalCity, cityMap):
    q = PriorityQueue() # Queue of Nodes
    total_cost= 0
    visited = set()

    # inserting beginningCity to the priorityqueue
    q.insert( [(beginningCity, 0, None), [[beginningCity, 0, None]]], 0)
    visited.add(beginningCity)

    # There is no need for search if start_point == destination
    if (beginningCity == goalCity):
		return result

    reached_dest = False
    while not reached_dest:
        # q.remove() will takeout the very first element that is in the priorityqueue
        currentCity = q.remove()
        cityname = currentCity[0][0]
        path_cost = currentCity[0][1]
        route = currentCity[0][2]
        path = currentCity[1]

        # add current city name to visited
        visited.add(cityname)

        # expand node of neighbors until goal node is reached
        # get the best key of all successors of node
        neighbors = getNeighbor(cityname, cityMap)
        neighbors = sorted(neighbors, key=itemgetter(1))
        # print neighbors

        # expanding all the node through the priorityqueue
        if neighbors:
            for neighbor in neighbors:
                if neighbor[0] not in visited:
                    cumul_cost = path_cost + neighbor[1]

                    neighbor = list(neighbor)
                    neighbor[1] = cumul_cost

                    q.insert([neighbor, currentCity[1] + [list(neighbor)]], cumul_cost)
                    # print currentCity[1] + [list(neighbor)]

                # if reached destination, terminate and add the neighbor to path
                if (neighbor[0] == goalCity):
                    reached_dest = True
                    path = currentCity[1] + [list(neighbor)]
                    break
            continue


    if (reached_dest):
        total_cost = cumul_cost

        total_seg = 0
        for i in range(1, len(path)):
            total_seg += 1
            print "- Take " + path[i][2] + " for " + str(path[i][1] - path[i-1][1]) + " miles to " + path[i][0]
        print "Total road segments: " + str(total_seg)
        print "Total distance: " + str(total_cost) + "miles"

    else:
        print('No goalCity reached\n')



if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "Wrong number of arguments"
        sys.exit()
    data = openFile('road-segments.txt')
    # print data

    start_city = sys.argv[1]
    end_city = sys.argv[2]
    algorithm = sys.argv[3]

    cityMap = {}
    processCityMap(data, cityMap)
    # print cityMap

    if sys.argv[3] == 'dfs':
        depthFirst(sys.argv[1], sys.argv[2], cityMap)

    if sys.argv[3] == 'bfs':
        breadthFirst(sys.argv[1], sys.argv[2], cityMap)

    if sys.argv[3] == 'best':
        best(sys.argv[1], sys.argv[2], cityMap)
