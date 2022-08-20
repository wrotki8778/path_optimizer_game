import os
import numpy as np
import pole

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')\
        or 'my-unique-pass'
    pole_borders = np.array([[-5,5],[-5,5]], dtype=np.single)
    targets = [pole.PathTarget(\
        centers = np.array([[1,0],[-1,1],[-3,3]]),name="first_target")]
    resistance = 1/2
    dt = 1/16
    pole1 = pole.Mountain(center= np.array([-2,1],\
                dtype=np.single),\
            height = 1,name="first_mountain")
    pole2 = pole.Mountain(center= np.array([3,-1],\
                dtype=np.single),\
            height = 1,name="second_mountain")
    poles = [pole1,pole2]
    
    