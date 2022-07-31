import numpy as np
import matplotlib.pyplot as plt

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
    def evaluate(self,pos):
        return(self.equation(pos,self.params))


class Mountain(Obstacle):
    def __init__(self,center,height,name):
        super(Mountain,self).__init__(mountain,[center,height],name)
    def show(self):
        plt.plot(self.params[0][0],self.params[0][1],'ro',\
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
    def show(self):
        plt.plot(self.params[0],self.params[1],'go')


class Game:
    def __init__(self,environment,obstacles):
        self.environment = environment
        self.obstacles = obstacles
    def pole_evaluate(self,pos):
        return sum([pole.evaluate(pos) for pole in self.obstacles])
    def dynamics(self,pos,speed):
        velocity = np.linalg.norm(speed)
        accel = self.pole_evaluate(pos) - self.environment.resistance\
            *velocity*np.array(speed)
        speed_next = speed + self.environment.dt * np.array(accel)
        pos_next = pos + self.environment.dt * np.array(speed)
        return pos_next,speed_next
    def stop_condition(self,pos,speed,time):
        out_of_bounds=  self.environment.out_of_bounds(pos)
        timeout = time > 16
        no_speed = np.linalg.norm(speed) < 1/16 and time > 1
        return(no_speed or timeout or out_of_bounds)
    def path_simulation(self,user_input):
        time = 0
        speed = [user_input[0],user_input[1]]
        pos = self.environment.origin
        hist_pos = pos
        while (not(self.stop_condition(pos,speed,time))):
            pos, speed = \
                self.dynamics(pos,speed)
            time += self.environment.dt
            hist_pos = np.vstack((hist_pos,pos))
        return [time,hist_pos,pos,speed]
        return(score)
    def print_report(self,user_input):
        time,hist_pos,pos,speed = self.path_simulation(user_input)
        score = 0
        for target in self.environment.targets:
            score = score + target.evaluate_score(hist_pos)
        print("Simulation has ended after {} seconds. The point is located at \
            {:4f}, {:4f} placement. The speed at the end was equal to {:4f}.\
                 Thank you for the participation!".format(time,pos[0],pos[1],np.linalg.norm(speed)))
        plt.close()
        plt.figure(0)
        plt.xlim(self.environment.borders[0,0],\
            self.environment.borders[0,1]),
        plt.ylim(self.environment.borders[1,0],\
            self.environment.borders[1,1])
        plt.plot(hist_pos[:,0],hist_pos[:,1], '--')
        for obstacle in self.obstacles:
            obstacle.show()
        for target in self.environment.targets:
            target.show()
        plt.title("Final score: %1.3f" %score)
        plt.savefig('app/static/images/foo.png')

def mountain(pos,params):
    center = params[0]
    magnitude = params[1]
    diff = pos-center
    if not diff.any():
        return np.array([0,0])
    else:
        distance = np.linalg.norm(diff)
        return np.exp(-distance**2)*magnitude*diff/distance

def dummy_pole(pos,params):
    return np.array([0,0])





