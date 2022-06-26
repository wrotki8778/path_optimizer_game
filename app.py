import pole
import numpy as np
import matplotlib.pyplot as plt
import flask

pole_borders = np.array([[-5,5],[-5,5]], dtype=np.single)
origin = [0,0]

environment = pole.Environment(pole_borders,origin,resistance=1/8,dt=1/4)

pole1 = pole.Obstacle(pole.mountain,[np.array([1,1]),5],"first_mountain")
pole2 = pole.Obstacle(pole.mountain,[np.array([2,-1]),8],"second_mountain")

poles = [pole1,pole2]


game = pole.Game(environment,poles)

game.print_report(np.array([1,1]))