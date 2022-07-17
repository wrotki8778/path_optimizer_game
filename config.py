import os
import numpy as np
import pole

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')\
        or 'my-unique-pass'
    pole_borders = np.array([[-5,5],[-5,5]], dtype=np.single)
    resistance = 1/2
    dt = 1/4
    pole1 = pole.Obstacle(pole.mountain,[np.array([1,1]),5],"first_mountain")
    pole2 = pole.Obstacle(pole.mountain,[np.array([2,-1]),8],"second_mountain")
    poles = [pole1,pole2]
    
    