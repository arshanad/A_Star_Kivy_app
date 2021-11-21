class AStarGraph(object):
	#Define a class board like grid with two barriers
        def __init__(self,barriers,rows,cols):
                self.barriers=[]
                self.barriers=barriers
                self.rows=rows
                self.cols=cols

        def heuristic(self, start, goal):
		#Use Chebyshev distance heuristic
                D = 1
                D2 = 1
                dx = abs(start[0] - goal[0])
                dy = abs(start[1] - goal[1])
                return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)
        def get_vertex_neighbours(self, pos):
                n = []
                for dx, dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]:
                        x2 = pos[0] + dx
                        y2 = pos[1] + dy
                        if x2 < 0 or x2 >= self.rows or y2 < 0 or y2 >= self.cols:
                          continue
                        n.append((x2, y2))
                return n
        def move_cost(self, a, b):
                for barrier in self.barriers:
                        if (b[0]==barrier[0] and b[1]==barrier[1]):
                                return 100 #Extremely high cost to enter barrier squares
                return 1 #Normal movement cost
