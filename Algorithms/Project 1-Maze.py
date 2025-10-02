import numpy as np
import random
from collections import deque

import matplotlib.pyplot as plt
import matplotlib.animation as animation

#Note: I will assign 2 maps: The Real Map and the Projected Map
class Maze:
    def __init__(self):
        self.M = None #The Map
        self.path = None #Tracking the Path
        
    def Generate_Maze(self,n,m):
        maze = np.ones((2*n+1,2*m+1)) #We generate the maze with Ones 
        maze[1][0] = 0 
        maze[-2][-1] = 0 
        start = (0,0) #The Starting Point
        maze[1][1] = 0 #Setting the (0,0) = 0,satisfying (2n+1,2m+1) = 0
        Stacks = [start] #Initiating DFS via Stacks
        while Stacks:
            directions = [(1,0),(-1,0),(0,1),(0,-1)]
            random.shuffle(directions) #Ensuring the path is randomized
            r,c = Stacks[-1] 
            for dr,dc in directions:
                nr = r + dr #Follow the row direction
                nc = c + dc #Follow the column direction
                if nr >= 0 and nc >= 0 and nr < n and nc < m and maze[2*nr+1][2*nc+1] != 0: #If the position has not been visited in real map
                    maze[2*nr+1][2*nc+1] = 0 #Mark as visited 
                    maze[2*r+1+dr][2*c+1+dc] = 0 #Opening the road
                    Stacks.append((nr,nc))
                    break
            else:
                Stacks.pop() #If action ran out, we remove by popping
        self.M = maze
    
    
    def Solve(self):
        directions = [(1,0),(-1,0),(0,1),(0,-1)] #Directions
        start = (1,1) #In the Projected Map, (0,0) -> (1,1)
        end = (self.M.shape[0]-1,self.M.shape[1]-1) #(the ending point)
        visited = np.zeros_like(self.M,dtype = bool) #This generate a 2D Matrix fits the Map with T-F,bool = 0-1 only
        visited[(1,1)] = True #Marking as visited
        queue = deque()
        queue.append((start,[])) #The Coordinate and the already-visited path
        while queue:
            node,path = queue.pop() #(r,c) and []
            for dr,dc in directions:
                next_node = (node[0] + dr,node[1] + dc) #(nr,nc)
                if next_node == end: #If the end has reached, break
                    self.path = path
                    return path
                
                if (next_node[0] >= 0 and next_node[1] >= 0 and next_node[0] < self.M.shape[0] and next_node[1] < self.M.shape[1] and self.M[next_node] == 0 and not visited[next_node]):
                    visited[next_node] = True
                    queue.append((next_node,path+[node])) #If new path is valid -> append in BFS
                    
    def draw_maze(self):
        fig,ax = plt.subplots(figsize = (10,10)) #Identifying the size of the figure within plt
        ax.imshow(self.M, cmap = plt.cm.binary, interpolation='nearest') #plotting the maze first

        ax.set_xticks([]) #setting x as None
        ax.set_yticks([]) #setting y as None
        if self.path:
            x = [x[1] for x in self.path] #column = x in cartesian
            y = [y[0] for y in self.path] #row = y in cartesian
            plt.plot(x,y,color='green',linewidth = 3)
        plt.show()
        
    def animate_maze(self):
        fig,ax = plt.subplots(figsize = (10,10))
        ax.imshow(self.M,cmap = plt.cm.binary,interpolation='nearest')
        
        ax.set_xticks([]) #setting x as None
        ax.set_yticks([]) #setting y as None
        
        if self.path is not None:
            line, = ax.plot([], [], color='green', linewidth=2)
            
            def init():
                line.set_data([], [])
                return line,
            
            def update(frame):
                x, y = self.path[frame] #path[0]'s data = (x,y
                line.set_data(*zip(*[(p[1], p[0]) for p in self.path[:frame+1]]))  # update the data with cartesian coordinate
                return line,
            
            ani = animation.FuncAnimation(fig, update, init_func=init,frames=range(len(self.path)), blit=True, repeat = False, interval=20)
            
        plt.show()
            
        

    
        
        
A = Maze()
A.Generate_Maze(50,5)
print(A.M)
print(A.Solve())
A.animate_maze()