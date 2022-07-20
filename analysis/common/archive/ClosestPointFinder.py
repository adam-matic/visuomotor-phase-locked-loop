import math
import numpy as np

def distance(p1, p2): 
    return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**0.5


class ClosestPointFinder():
    def __init__(self, path, pt, jump_limit = 200):
        if len(path) == 2:
            self.path  = list(zip(*path))  # convert (xs, ys) to [(x0, y0),..(xn,yn)] 
        else:
            self.path = path

        self.N     = len(self.path)    # number of points
        
        # init closest point
        rng        = range(0, self.N)     
        dists      = [ distance(pt, self.path[i]) for i in rng]
        self.ci    = rng[np.argmin(dists)]      # init index of the closest point
        self.cp    = self.path[self.ci]         # init closes point coordinates
        self.absd  = min(dists)                 # distance

        self.d    = 0                 # initial distance of the closest point
        self.prev_d = 0               # previous distance
        self.distances = [self.absd]  # list of previous distances
        self.prev_cp = self.cp        # previous closest point
        self.cps = [self.cp]          # list of previous closest points?
        self.v   = [0, 0]             # velocity
        self.vs  = []                 # list of velocities
        self.vx, self.vy = 0, 0       # speed
        self.pvx, self.pvy = 0, 0     # previous speed
        self.cis = [self.ci]          # list of indexes of closest points
        self.dci = 0                  # rate of change of ci, init
        
        self.jumps = 0
        self.jump_limit = jump_limit
        self.cycle_pos = 0.0

    def find_next_closest(self, pt):
        if self.absd > self.jump_limit:
            self.jumps += 1 
            imin, imax = 0, self.N
        else:
            if self.dci > 0:
                self.forward_look =  int(self.dci + 10 ) * 3 
                self.backward_look =  -int(self.dci + 10) 
            elif self.dci < 0:
                self.forward_look =  -int(self.dci - 10)  
                self.backward_look =  int(self.dci - 10 ) * 3
            else:
                self.forward_look = 100
                self.backward_look = -100

            imax = (self.ci + self.forward_look)  % self.N
            imin = (self.ci + self.backward_look) % self.N
        if imin > imax:
            rng = list ( range(imin, self.N)) + list(range(0, imax))
        else:
            rng = list ( range (imin, imax))
        
        self.rng = rng
        dists      = [ distance(pt, self.path[i]) for i in rng]
        self.ci    = rng[np.argmin(dists)] 
        self.cp    = self.path[self.ci]
        self.absd  = min(dists)               
        
        # rate of change of ci
        self.cis.append(self.ci)
        self.cps.append(self.cp)
        dc = (self.cis[-1] - self.cis[-2]) 
        self.dc = dc
        if dc > self.N/2: dc = dc % -self.N
        elif dc < -self.N/2: dc = dc % self.N
        self.cycle_pos += (dc / self.N)
        self.dci = self.dci + ( dc - self.dci) / 30

        # to get signed distance, use movement direction (velocity)
        vx = self.cp[0] - self.prev_cp[0]   # x
        vy = self.cp[1] - self.prev_cp[1]   # y  <<< use QPoints??
        
        if (vx * vy == 0): vx, vy = self.pvx, self.pvy  ## is this necessary??
        self.pvx, self.pvy = vx, vy
        self.prev_cp = self.cp

        Dx = pt[0] - self.cp[0]
        Dy = pt[1] - self.cp[1]
        
        va = math.atan2(vy, vx) % ( 2 * math.pi )
        da = math.atan2(Dy, Dx) % ( 2 * math.pi ) 

        d_angle = (va - da) % ( 2 * math.pi )
        sign = 1 if d_angle > math.pi else -1
        
        self.prev_d = self.d
        self.d = sign * self.absd
        self.distances.append(self.d)
        #self.vs.append([vx, vy])
        
        return self.d

    def run(self, cx, cy):
        for i in range(1, len(cx)):
            self.find_next_closest((cx[i], cy[i]))
        self.distances[0] = self.distances[0] * np.sign(self.distances[1])
        #return self