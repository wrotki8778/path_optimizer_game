import numpy as np
pole_borders = np.array([[-1000,1000],[-1000,1000]], dtype=np.single)
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
    return mountain(point,np.array([1,1]),40)

def pole2(point):
    return mountain(point,np.array([2,-1]),30)

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
    no_speed = np.linalg.norm(speed) < 1/64 and time > 1
    return(no_speed or timeout or out_of_bounds)


def path_simulation(poles,origin,dt=1/4,resistance=1/16):
    time = 0
    pos = origin
    speed = np.array([0,0])
    while (not(stop_condition(pole_borders,pos,speed,time))):
        pos, speed = \
            dynamics(poles,pos,speed,dt=dt,resistance=resistance)
        time += dt
    print("Simulation has ended after {} seconds. The point is located at \
            {}, {} placement. Thank you for the participation!".format(time,pos[0],pos[1]))

path_simulation(poles,np.array([0,0]),dt=1/8, resistance = 1/16)


