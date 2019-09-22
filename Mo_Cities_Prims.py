'''########################################
Cole Davis

This file contains code that reads in graph Latitude and Longitude information of 961 different Missouri cities, townships, villages, etc. from a .dat file.
A graph representation of the cities is created with an adjacency list. There is an edge between every city that is within 30 miles of it. A minimum spanning tree is computed 
using Prim's algorithm using the adjacency list. The minimum spanning tree is then displayed using the Python Library matplotlib. 
###########################################'''


'''#######################################################'''
#TODO: refactor functionality into functions/multiple files
'''#######################################################'''



'''################
       Setup
###################'''
DEBUG1 = True #This controls whether or not the original graph is shown
DEBUG2 = True #This outputs the adjacency list to a text file for funsies

import time
import math
import random

import matplotlib.pyplot as plt
plt.xlim([0, 99950932])
plt.ylim([0, 99950932])
plt.ylabel('Latitude')
plt.xlabel('Longitude')


'''######################################
       GRAPH DATA STORAGE CLASSES
##########################################'''
class City:    
  def __init__(self, name, lat, lon, ID): 
    self.name = name
    self.lat = int(lat)
    self.lon = int(lon)
    self.ID = int(ID)

#This class contains a list of pair objects.
class LinkedList:
    def __init__(self):
        self.data = list()

    def AddConn(self, cityID1, cityID2, dist):
        self.data.append(Edge(cityID1, cityID2, dist)) #AddConn is currently only used for MatplotLib visualization

    def ShowGraph(self, Cities, x):
        xcoor = [] #Used for matplotlib
        ycoor = [] #Used for matplotlib
         
        #Plot city x (not starting city)
        plt.scatter(Cities[x].lat, Cities[x].lon,  color = "g")  

        #Plot the connections that each city, x, has
        for i in range(len(self.data)):
            xcoor = [Cities[x].lat, Cities[self.data[i].cityID2].lat]
            ycoor = [Cities[x].lon, Cities[self.data[i].cityID2].lon]
            plt.plot(xcoor,ycoor,'r-', linewidth = 0.3) #'ro-' originally            


#An array of Edge objects will be how the MST is represented
class Edge:
    def __init__(self, cityID1, cityID2, dist):
        self.cityID1 = cityID1
        self.cityID2 = cityID2
        self.dist = dist
        self.added = False


'''###################################
         Debug Functions
#####################################'''
#Print out all city information
def PrintCities():
    for city in Cities:
        print(city.name)
        print("Lat:",city.lat)
        print("Lon:",city.lon)
        print("ID: ",city.ID)
        print()
        print()

def PrintMatrix(DistMatrix):    
    for x in range(NUM_CITIES):
        print(DistMatrix[x])
    print()
    print()

 
    
'''###################################
         Arithmetic Functions
#####################################'''
#Distance Formula calculation
def DistFormula(x1, y1, x2, y2, CONVERSION):
    result = (math.sqrt((x1-x2)**2 + (y1-y2)**2))/CONVERSION
    return result


'''####################################################
      Utility Functions (Formatting things correctly
########################################################'''
#Makes the 2D matrix symmetrical again (Due to "every node connected to at least one other node" check)
def Symmetrify(DistMatrix):
    for x in range(NUM_CITIES):
        for y in range(NUM_CITIES):
            if(x != y):
                if(not(DistMatrix[x][y] == None and DistMatrix[y][x] == None)):         #Don't continue if both cells have "None" in them
                    
                    if(DistMatrix[x][y] == None and DistMatrix[y][x] != None):          #if One of the nodes is the smallest connection to the other one, make graph symmetrical again
                        DistMatrix[x][y] = DistMatrix[y][x]

                    elif(DistMatrix[x][y] != None and DistMatrix[y][x] == None):        #if One of the nodes is the smallest connection to the other one, make graph symmetrical again
                        DistMatrix[y][x] = DistMatrix[x][y]
                  

#Uses matplotlib to visualize the mimimum spanning tree
def ShowMST(Cities, Solution):
    OFFSET = 5000000 
    xcoor = [] 
    ycoor = [] 

    print("##################     Edges in the MST     ###################")
    for i in range(len(Solution)):
        if(Solution[i].cityID1 == None):
            print("Started at ",Cities[Solution[i].cityID2].name)
            plt.scatter(Cities[Solution[i].cityID2].lat+OFFSET, Cities[Solution[i].cityID2].lon, color = "g")
        else:
            plt.scatter(Cities[Solution[i].cityID2].lat+OFFSET, Cities[Solution[i].cityID2].lon, color = "r")
            xcoor = [Cities[Solution[i].cityID1].lat+OFFSET, Cities[Solution[i].cityID2].lat+OFFSET]
            ycoor = [Cities[Solution[i].cityID1].lon, Cities[Solution[i].cityID2].lon]
            plt.plot(xcoor,ycoor,'b-', linewidth = 0.3) 
    print("There are ",len(Solution)-1,"edges in the MST") #I'm subtracting one because the starting node has a "None" as the start point
      

'''###################################
         MIN-HEAP FUNCTIONS
#####################################'''
'''
    Initialization of min_heapify:
    Every node i+1, i+2, i+3,...,i+n is the root of a min heap.
    Since i is equal to n at initialization, there are no children 
    nodes to evaluate so vacuously true.
'''
def min_heapify(A, i): #Called when the root node is removed
    if(len(A) == 0):
        return;
    else:
        #print("Evaluating ",A[i], " index ",i)
        left = 2 * i + 1
        right = 2 * i + 2
        largest = i

        #Determine larger child
        if left < len(A) and A[left].dist < A[largest].dist:
            largest = left

        if right < len(A) and A[right].dist < A[largest].dist:
            largest = right

        #Swap the larger child and the parent if child > parent
        if largest != i:
            temp1 = A[i]            
            A[i] = A[largest]
            A[largest] = temp1

           
            #Now see if the child you just swapped needs to swap with its child (continue sifting down)
            min_heapify(A, largest) 
    


'''
Invariants of pop(): same as min_heapify
'''
def pop(Arr):
    if(len(Arr) != 0):
        #Replace first index with last element
        Arr[0] = Arr[len(Arr)-1]

        #Remove the last element that just was sifted up to root
        del Arr[-1]

        #Sift the root downwards with its larger children until it finds its spot
        min_heapify(Arr, 0)
    else:
        print("Trying to pop an empty heap")


'''
    Initialization of add:
    Every node i+1, i+2, i+3,...,i+n is the root of a min heap.
    Since i is equal to n at initialization, there are no children 
    nodes to evaluate so vacuously true.
'''
#Adds an edge object to the Min Heap
def add(Arr, edge): 

    child = len(Arr)
    parent = ((len(Arr))-1)//2
    Arr.append(edge)

    while(Arr[parent].dist > edge.dist and parent >= 0):
        temp = Arr[parent]
        Arr[parent] = edge
        Arr[child] = temp

        #Reset indexes for next sift up
        child = parent
        parent = (parent-1)//2


'''###################################
         Other Functionality
#####################################'''
def find(cityID2, Solution):
    found = False    #Linear search through Solution, looking for cityID2

    for i in range(len(Solution)):
        if(Solution[i].cityID2 == cityID2):
            found = True 
            break
    return(found)

    
'''###################################################################################################
         Consts, Reading in Graph Data from .dat file, Creating Adjacency List and Adjacency Matrix.
         (Adj. Matrix is only used to create the Adj. list and find the smallest connection each node has)
#######################################################################################################'''
#Consts
MILE_CONVERSION = 17013   #Approximately one mile when using lat & lon conversion to decimal form 
RADIUS = 30    #30 
NUM_CITIES =961 #961

#Cities[] and adj. matrix initialization
DistMatrix = [[0 for x in range(NUM_CITIES)] for y in range(NUM_CITIES)] #Initialize the adj. matrix with all zeroes
DistList = []                                                            #Initialize the adj. list blank. (This list will hold 961 LinkedList Objects)
Cities = []                                                              #Holds all city info
SmallestConn = []                                                        #Holds 961 Pair objects containing the shortest connection for each city


#Populate Cities[] with all city objects
File = open("both.dat", "r+") #both.dat is the actual one
#File2 = open("Matrix.txt", "w")    #Find a way to prettily write out the adjacency matrix to a text file (It's cool to have) 
File3 = open("Adjacency.txt","w")   #Find a way to prettily rite out the adjacency list to a text file (Also cool to have)
for i in range(NUM_CITIES):
    name = File.readline()
    lat = File.readline()
    lon = File.readline()
    Cities.append(City(name, lat, lon, i))


#Calculate the distance from every city to every other city
for x in range(NUM_CITIES):
    for y in range(NUM_CITIES):
        if(x != y): #Don't calulate distance from itself
            DistMatrix[x][y] = DistFormula(Cities[x].lat, 
                                           Cities[x].lon,
                                           Cities[y].lat,
                                           Cities[y].lon,
                                           MILE_CONVERSION)

#Make sure every city is connected to at least one other city (If a city has only connections greater than 30, let that city keep its one shortest connection)
for x in range(NUM_CITIES):
    smallest_conn = 9999999
    cityID1 = x # Outer x Index
    cityID2 = -1 # Inner y Index
    for y in range(NUM_CITIES):
        #Don't include connection with itself
        if(x != y): 
            if(DistMatrix[x][y] < smallest_conn):
                smallest_conn = DistMatrix[x][y]
                cityID2 = y
            #Now that all distances have been iterated over for city X, append its smallest connection to SmallestConn[]
            if(y == NUM_CITIES - 1):
                SmallestConn.append(Edge(cityID1, cityID2, smallest_conn))
        #Edge case for bottom right matrix cell (due to my x!=y check previously)
        elif(x == NUM_CITIES-1):
            SmallestConn.append(Edge(cityID1, cityID2, smallest_conn))

                
#Keep only the connections that are <= 30 miles. (Adjacency Matrix is created. Adjacency List will be created from this data.)
for x in range(NUM_CITIES):
    for y in range(NUM_CITIES):
        if(DistMatrix[x][y] > RADIUS):
            DistMatrix[x][y] = None


#Reapply the smallest connection for every city (make sure every city is connected to the graph)
for x in range(NUM_CITIES):
    DistMatrix[x][SmallestConn[x].cityID2] = SmallestConn[x].dist
    #print("Smallest connection for ",Cities[x].name," is ",SmallestConn[x].dist, " with ", Cities[SmallestConn[x].cityID].name)


#Make the Matrix symmetrical again (if x connects to y, then y must connect to x and vice verse)
Symmetrify(DistMatrix)


#Create Adjacency List from DistMatrix's data
for x in range(NUM_CITIES):
    DistList.append(LinkedList())
    for y in range(NUM_CITIES):
        if(DistMatrix[x][y] != None and DistMatrix[x][y] != 0): #Don't connect to itself (that's what "and DistMatrix[x][y] does)
            DistList[x].AddConn(x, y, DistMatrix[x][y])     #Append the ID of cityX, cityY, and distance from cityX from cityY: (DistMatrix[x][y] variable)
        

#Print out of the adjecency list
for x in range(NUM_CITIES):
    if(DEBUG1): #Matplotlib the original graph
        print(x,": ",Cities[x].name)
        DistList[x].ShowGraph(Cities, x)

if(DEBUG2):
    total_num_edges = 0
    #Plot the connections that city x has
    for i in range(len(DistList)):
        print("Writing to adjecency list file",i)
        File3.write("\n\n\n\n")
        File3.write(Cities[i].name + "\n")
        for q in range(len(DistList[i].data)):
            File3.write(str(DistList[i].data[q].cityID2)+"\t")
            total_num_edges = total_num_edges+1
if(DEBUG2):
    print("The average number of connections is: ",total_num_edges/961)




'''
##############################################
         Prim's Driver 
##############################################
'''

print("STARTING NOW")
start = time.time()
Solution = []    #Stores all edges that are part of the MST each iteration
PQ = []       #The min heap (Priority queue) used to store the currently visible edges

startingCityID = 0 #This is for selecting the starting city




'''#################################
         Prim's Algorithm
#################################'''

'''Add Arbitrary Starting City'''
Solution.append(Edge(None, startingCityID, 9999999))  

'''
INITIALIZATION (Prim's):
A single node with no edges is trivially a minimum Spanning Tree, so initialization holds.

Precondition: There is a graph with at least one node to operate on.
'''

#Add each edge of starting node's edges to the Priority Queue
for i in range(len(DistList[startingCityID].data)): 
    add(PQ, DistList[startingCityID].data[i])       


'''Now do the rest of the graph'''
#NUM_CITIES-1 edges will be the size of finished MST 
for q in range(NUM_CITIES-1):
    if(len(PQ) > 0):
        while(find(PQ[0].cityID2, Solution) and len(PQ) > 1): #Don't add edge to solution array if the node we're checking is already in the solution array (that would make a cycle)
            pop(PQ)
        
        Solution.append(PQ[0])  #Add edge to MST
        print("Added edge",q,"of",NUM_CITIES-1)

        newEdge = PQ[0] #Store the values of the edge we just added
        pop(PQ)

        for i in range(len(DistList[newEdge.cityID2].data)):    #Add all the new edges into the PQ
            add(PQ, DistList[newEdge.cityID2].data[i]) 

'''
TERMINATION (Prim's):
Since every edge was added greedily, and each edge that was added did not create a cycle, the result must be a minimum spanning tree, so Termination holds.

Postcondition: The result is a minimum spanning tree.
'''


end = time.time()
print("Starting at ", Cities[startingCityID].name,"ran in ",end-start,"seconds")


#Display the MST
ShowMST(Cities, Solution)


File.close()
#File2.close()
File3.close()
plt.show()
