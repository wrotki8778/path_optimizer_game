import os
import numpy as np
import pole

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')\
        or 'my-unique-pass'
    pole_borders = np.array([[-5,5],[-5,5]], dtype=np.single)
    targets = [pole.PointTarget(center = [1,0],name="first_target"),
                pole.PointTarget(center = [-1,-1],name="second_target")]
    resistance = 1/2
    dt = 1/4
    pole1 = pole.Mountain(center= np.array([1,1]),\
            height = 5,name="first_mountain")
    pole2 = pole.Mountain(center= np.array([2,-1]),\
            height = 8,name="second_mountain")
    poles = [pole1,pole2]
    
    