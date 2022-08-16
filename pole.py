import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation,PillowWriter

class Environment:
    def __init__(self, borders, targets, origin, resistance, dt):
        self.borders = borders
        self.targets = targets
        self.origin = origin
        self.resistance = resistance
        self.dt = dt
    def out_of_bounds(self,pos):
        return(self.borders[0,0]>pos[0] \
                    or self.borders[0,1]<pos[0] \
                    or self.borders[1,0]>pos[1] \
                    or self.borders[1,1]<pos[1])

class Obstacle:
    def __init__(self,equation,params,name):
        self.equation = equation
        self.params = params
        self.name = name
    def evaluate(self,x,y):
        return(self.equation(x,y,self.params))


class Mountain(Obstacle):
    def __init__(self,center,height,name):
        super(Mountain,self).__init__(mountain,[center,height],name)
    def show(self,graph):
        graph.plot(self.params[0][0],self.params[0][1],'ro',\
            ms=self.params[1])

class Target(Obstacle):
    def __init__(self,params,name):
        super(Target,self).__init__(dummy_pole,params,name)
       

class PointTarget(Target):
    def __init__(self,center,name):
        super(PointTarget,self).__init__(params=center,name=name)
    def evaluate_score(self,path):
        score = min((path[:,0] - self.params[0]) ** 2\
                + (path[:,1] - self.params[1]) ** 2)
        return score
    def show(self,graph):
        graph.plot(self.params[0],self.params[1],'go')


class Game:
    def __init__(self,environment,obstacles):
        self.environment = environment
        self.obstacles = obstacles
    def pole_evaluate(self,x=0,y=0):
        stacked_poles = np.stack([pole.evaluate(x,y)\
            for pole in self.obstacles],axis=-1)
        return np.transpose(np.sum(stacked_poles,axis=-1))
    def dynamics(self,pos=np.array([0,0],dtype=np.single)\
        ,speed=0):
        velocity = np.linalg.norm(speed)
        accel = self.pole_evaluate(pos[0],pos[1]) - self.environment.resistance\
            *velocity*np.array(speed)
        speed_next = speed + self.environment.dt * np.array(accel)
        pos_next = pos + self.environment.dt * np.array(speed)
        return pos_next,speed_next
    def stop_condition(self,pos,speed,time):
        out_of_bounds=  self.environment.out_of_bounds(pos)
        timeout = time > 16
        return(timeout or out_of_bounds)
    def path_simulation(self,user_input):
        time = 0
        speed = [user_input[0],user_input[1]]
        pos = self.environment.origin
        hist_pos = np.insert(pos,0,time,axis=0)
        while (not(self.stop_condition(pos,speed,time))):
            time += self.environment.dt
            pos, speed = \
                self.dynamics(pos,speed)
            hist_pos = np.vstack((hist_pos,np.insert(pos,0,time,axis=0)))
        return [time,hist_pos,pos,speed]
    def take_a_snapshot(self,hist_pos):
        score = 0
        for target in self.environment.targets:
            score = score + target.evaluate_score(hist_pos)
        fig,ax=plt.subplots()
        def animate(i):
            ax.clear()
            ax.set_xlim(self.environment.borders[0,0],\
                self.environment.borders[0,1]),
            ax.set_ylim(self.environment.borders[1,0],\
                self.environment.borders[1,1])
            arg_xy = np.stack([np.repeat(np.linspace(\
                self.environment.borders[0,0],\
                self.environment.borders[0,1],11),11)\
                    .reshape(11,11,order='F')\
                    .reshape(121),\
                np.repeat(np.linspace(\
                self.environment.borders[0,0],\
                self.environment.borders[0,1],11),11)\
                    .reshape(11,11,order='C')\
                    .reshape(121)],axis=1)
            vec_xy = self.pole_evaluate(arg_xy[:,0],arg_xy[:,1])
            ax.quiver(arg_xy[:,0].reshape(11,11),\
                arg_xy[:,1].reshape(11,11),
                vec_xy[:,0].reshape(11,11),
                vec_xy[:,1].reshape(11,11)
                )
            line, = ax.plot(hist_pos[0:i,1],hist_pos[0:i,2], '--')
            for obstacle in self.obstacles:
                obstacle.show(ax)
            for target in self.environment.targets:
                target.show(ax)
            ax.set_title("Time: %1.3f Score: %1.3f" %(hist_pos[i,0],score))
            return line,
        animation = FuncAnimation(fig,animate,blit=True\
            ,repeat=False,interval=40,frames=len(hist_pos[:,0]))
        animation.save("app/static/images/foo.gif",dpi=100,writer=PillowWriter(fps=25))

def mountain(x,y,params=[[0,0],1]):
    return \
        np.array((x-params[0][0],\
         y-params[0][1]))\
        * params[1] \
        * np.exp(- np.sqrt(
              (x-params[0][0])**2 \
            + (y-params[0][1])**2 ))\
        / ( np.sqrt( (x-params[0][0])**2 \
           + (y-params[0][1])**2 ) \
           + 0.001)

def dummy_pole(x,y,params):
    return np.array([0,0],dtype=np.single)




