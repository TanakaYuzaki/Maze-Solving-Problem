import numpy as np
import random
from collections import deque

import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Maze:
    def __init__(self):
        self.map = None #The Map
        self.path = None #The Path tracking
        self.r_size = None #The Row Size
        self.c_size = None #The Column Size

    def Random_Maze_Generator(self,r,c):
        self.r_size = r #Row 
        self.c_size = c #Column
        directions = [(0,1),(0,-1),(1,0),(-1,0)] #The direction in 2D
        Map = np.ones((2*r+1,2*c+1)) #Considering the walls 
        Start = (0,0)
        Map[1][1] = 0 #The Starting Point in the Matrix
        End = (r-1,c-1) #The Ending point
        Stack = [Start]

        while Stack:
            cur_r,cur_c = Stack[-1]
            random.shuffle(directions)
            for dr,dc in directions:
                new_r = cur_r + dr
                new_c = cur_c + dc
                if new_r >= 0 and new_c >= 0 and new_r < r and new_c < c and Map[2*new_r+1][2*new_c+1] == 1: #If the new cell hasn't been visited yet
                    Map[2*new_r+1][2*new_c+1] = 0
                    Map[2*cur_r+1 +dr][2*cur_c+1+dc] = 0
                    Stack.append((new_r,new_c))
                    break
            else:
                Stack.pop()
        self.map = Map #Saving the map

        Dict = self.Check_Maze()

        print(Dict[0]/(Dict[0]+Dict[1]))
            

    def Check_Maze(self):
        dict = {}
        for i in range(1,2*self.r_size):
            for j in range(1,2*self.c_size):
                if self.map[i][j] not in dict:
                    dict[self.map[i][j]] = 1
                else:
                    dict[self.map[i][j]] += 1
        return dict       
            
        
        
    

    def BFS(self):
        directions = [(0,1),(0,-1),(1,0),(-1,0)]
        visited = np.zeros_like(self.map,dtype=bool)
        start = (0,0)
        end = (self.r_size-1,self.c_size-1)
        queue = deque()
        queue.append((start,[start]))
        while queue:
            (cur_r,cur_c),path = queue.popleft()
            visited[2*cur_r+1][2*cur_c+1] = True
            for dr,dc in directions:
                new_r = cur_r +dr
                new_c = cur_c + dc
                if  new_r >= 0 and new_c >= 0 and new_r < self.r_size and new_c < self.c_size and visited[2*new_r+1][2*new_c+1] == False  and self.map[2*new_r+1][2*new_c+1] == 0 and self.map[2*cur_r+1+dr][2*cur_c+1+dc] == 0:
                    if new_r == end[0] and new_c == end[1]:
                        path.append((new_r,new_c))
                        self.path = path
                        return True
                    path.append((new_r,new_c))
                    queue.append(((new_r,new_c),path))
        
    
                



    

        
        


    
A = Maze()
print(A.Random_Maze_Generator(10,10))

print(A.Check_Maze())
