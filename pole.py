import numpy as np
import matplotlib.pyplot as plt

class Environment:
    def __init__(self, borders, origin, resistance, dt):
        self.borders = borders
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

class Game:
    def __init__(self,environment,obstacles):
        self.environment = environment
        self.obstacles = obstacles
    def pole_evaluate(self,pos):
        return sum([pole.evaluate(pos) for pole in self.obstacles])
    def dynamics(self,pos,speed):
        velocity = np.linalg.norm(speed)
        accel = self.pole_evaluate(pos) - self.environment.resistance\
            *velocity*speed
        speed_next = speed + self.environment.dt * accel
        pos_next = pos + self.environment.dt * speed
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
    def print_report(self,user_input):
        time,hist_pos,pos,speed = self.path_simulation(user_input)
        print("Simulation has ended after {} seconds. The point is located at \
            {:4f}, {:4f} placement. The speed at the end was equal to {:4f}.\
                 Thank you for the participation!".format(time,pos[0],pos[1],np.linalg.norm(speed)))
        plt.plot(hist_pos[:,0],hist_pos[:,1], 'bo')
        plt.savefig('foo.png')

def mountain(pos,params):
    center = params[0]
    magnitude = params[1]
    diff = pos-center
    if not diff.any():
        return np.array([0,0])
    else:
        distance = np.linalg.norm(diff)
        return np.exp(-distance**2)*magnitude*diff/distance




