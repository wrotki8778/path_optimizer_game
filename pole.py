import numpy as np
import matplotlib.pyplot as plt
pole_borders = np.array([[-5,5],[-5,5]], dtype=np.single)
origin = [0,0]

def mountain(pos,center,magnitude):
    diff = pos-center
    if not diff.any():
        return np.array([0,0])
    else:
        distance = np.linalg.norm(diff)
        return np.exp(-distance**2)*magnitude*diff/distance

def pole_equation(poles,point):
    return sum([pole(point) for pole in poles])

def pole1(point):
    return mountain(point,np.array([1,1]),5)

def pole2(point):
    return mountain(point,np.array([2,-1]),8)

poles = [pole1,pole2]

def dynamics(poles,pos,speed,dt=1/4,resistance=1/16):
    velocity = np.linalg.norm(speed)
    accel = pole_equation(poles,pos) - resistance*velocity \
            * speed
    speed_next = speed + dt * accel
    pos_next = pos + dt * speed
    return pos_next,speed_next

def stop_condition(pole_borders,pos,speed,time):
    out_of_bounds=  pole_borders[0,0]>pos[0] \
                    or pole_borders[0,1]<pos[0] \
                    or pole_borders[1,0]>pos[1] \
                    or pole_borders[1,1]<pos[1]
    timeout = time > 16
    no_speed = np.linalg.norm(speed) < 1/16 and time > 1
    return(no_speed or timeout or out_of_bounds)


def path_simulation(poles,origin,dt=1/4,resistance=1/16):
    time = 0
    pos = origin
    hist_pos = pos
    speed = np.array([0,0])
    while (not(stop_condition(pole_borders,pos,speed,time))):
        pos, speed = \
            dynamics(poles,pos,speed,dt=dt,resistance=resistance)
        time += dt
        hist_pos = np.vstack((hist_pos,pos))
    print("Simulation has ended after {} seconds. The point is located at \
            {:4f}, {:4f} placement. The speed at the end was equal to {:4f}.\
                 Thank you for the participation!".format(time,pos[0],pos[1],np.linalg.norm(speed)))
    plt.plot(hist_pos[:,0],hist_pos[:,1], 'bo')
    plt.savefig('foo.png')
results = path_simulation(poles,np.array([1,0]),dt=1/2, resistance = 1/8)


