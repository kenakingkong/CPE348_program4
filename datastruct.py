import sys
import os

class Graph:
    def __init__(self):
        self.vertices = {}
        self.numVertices = 0
        self.time = 0

    #read specifications for graph in file
    def read_graph(self, filename):
        
        infile = open(filename, "r")

        line1 = infile.readline().rstrip()
        n = int(line1)
        line2 = infile.readline().rstrip()
        e = int(line2)

        for i in range(1,n+1): 
            self.addVertex(i)

        for j in range(0,e):
            newline = infile.readline()
            eData = newline.split()
            self.addEdge(int(eData[0]), int(eData[1]), int(eData[2]))
            

    #return list of lists
    #[int key, distance from start, int key for predecessor]
    def short_paths(self, start_vertex):
        
        result = []
        pq = PriorityQueue()
        start = self.getVertex(start_vertex)
        start.setDistance(0)
        start.setPred(start)
        pq.buildHeap([(self.getVertex(v).getDistance(), v) for v in self.vertices]) 

        while not pq.isEmpty():
            minV = pq.delMin()
            currentV = self.getVertex(minV)
            for eachV in currentV.getConnections():
                temp = currentV.getDistance() + currentV.getWeight(eachV)
                if temp < eachV.getDistance():
                    eachV.setDistance(temp)
                    eachV.setPred(currentV) 
                    pq.decreaseKey(eachV, temp)

        for v in self.getVertices():
            vert = self.getVertex(v)
            result.append([v, vert.getDistance(), vert.getPred().getId()])        

        return result


    def addVertex(self,key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertices[key] = newVertex
        return newVertex
    
    def getVertex(self,n):
        if n in self.vertices:
            return self.vertices[n]
        else:
            return None

    def __contains__(self,n):
        return n in self.vertices
    
    def addEdge(self,f,t,cost):
            if f not in self.vertices:
                nv = self.addVertex(f)
            if t not in self.vertices:
                nv = self.addVertex(t)
            self.vertices[f].addNeighbor(self.vertices[t],cost)
            self.vertices[t].addNeighbor(self.vertices[f],cost)
    
    def getVertices(self):
        return list(self.vertices.keys())
        
    def __iter__(self):
        return iter(self.vertices.values())


class Vertex:
    def __init__(self, num):
        self.id = num
        self.connectedTo = {}
        self.dist = sys.maxsize         # distance to start
        self.pred = None         # previous node
        self.disc = 0
        self.conn_comp = 0

    def addNeighbor(self, nbr, weight):
        self.connectedTo[nbr] = weight

    def setDistance(self, d):
        self.dist = d

    def getDistance(self):
        return self.dist

    def getConnections(self):
        return self.connectedTo.keys()

    def getWeight(self,nbr):
        return self.connectedTo[nbr]

    def getPred(self):
        return self.pred

    def setPred(self,p):
        self.pred = p

    def setDiscovery(self,dtime):
        self.disc = dtime

    def getDiscovery(self):
        return self.disc

    def getId(self):
        return self.id

    def __str__(self):
       return str(self.id) + ": " + str(self.dist)# + " pred: " + str(self.pred)


class PriorityQueue:
    def __init__(self):
        self.heapArray = [(0,0)]
        self.currentSize = 0

    def buildHeap(self,alist):
        self.currentSize = len(alist)
        self.heapArray = [(0,0)]
        for i in alist:
            self.heapArray.append(i)
        i = len(alist) // 2            
        while (i > 0):
            self.percDown(i)
            i = i - 1
                        
    def percDown(self,i):
        while (i * 2) <= self.currentSize:
            mc = self.minChild(i)
            if self.heapArray[i][0] > self.heapArray[mc][0]:
                tmp = self.heapArray[i]
                self.heapArray[i] = self.heapArray[mc]
                self.heapArray[mc] = tmp
            i = mc
                
    def minChild(self,i):
        if i*2 > self.currentSize:
            return -1
        else:
            if i*2 + 1 > self.currentSize:
                return i*2
            else:
                if self.heapArray[i*2][0] < self.heapArray[i*2+1][0]:
                    return i*2
                else:
                    return i*2+1

    def percUp(self,i):
        while i // 2 > 0:
            if self.heapArray[i][0] < self.heapArray[i//2][0]:
               tmp = self.heapArray[i//2]
               self.heapArray[i//2] = self.heapArray[i]
               self.heapArray[i] = tmp
            i = i//2
 
    def add(self,k):
        self.heapArray.append(k)
        self.currentSize = self.currentSize + 1
        self.percUp(self.currentSize)

    def delMin(self):
        retval = self.heapArray[1][1]
        self.heapArray[1] = self.heapArray[self.currentSize]
        self.currentSize = self.currentSize - 1
        self.heapArray.pop()
        self.percDown(1)
        return retval
        
    def isEmpty(self):
        if self.currentSize == 0:
            return True
        else:
            return False

    def decreaseKey(self,val,amt):
        # this is a little wierd, but we need to find the heap thing to decrease by
        # looking at its value
        done = False
        i = 1
        myKey = 0
        while not done and i <= self.currentSize:
            if self.heapArray[i][1] == val:
                done = True
                myKey = i
            else:
                i = i + 1
        if myKey > 0:
            self.heapArray[myKey] = (amt,self.heapArray[myKey][1])
            self.percUp(myKey)
            
    def __contains__(self,vtx):
        for pair in self.heapArray:
            if pair[1] == vtx:
                return True
        return False


#g = Graph()
#g.read_graph("mytest.txt")
#print(g.short_paths(1))
