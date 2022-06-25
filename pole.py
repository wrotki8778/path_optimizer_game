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

print(dynamics(poles,np.array([0,0]),np.array([1,0])))

