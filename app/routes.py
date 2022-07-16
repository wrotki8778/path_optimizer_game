from flask import render_template, flash, redirect, url_for,request
from app import app
from app.forms import form_test
import numpy as np
import matplotlib.pyplot as plt
import pole

@app.route('/', methods = ['GET','POST'])
@app.route('/parameter', methods = ['GET','POST'])
def grab_parameters():
    form = form_test()
    if form.validate_on_submit():
        flash('Position vector: ({},{}),\
            vector initial speed: ({},{})'\
                .format(form.position1.data,form.position2.data\
                    ,form.speed_amplitude.data,form.speed_phase.data))
        pos_init = [float(request.form['position1']),\
            float(request.form['position2'])]
        speed_init = [float(request.form['speed_amplitude']),\
            float(request.form['speed_phase'])]
        return redirect(url_for('evaluate',pos_init=pos_init\
            ,speed_init = speed_init))
    return(render_template('parameter.html', \
        title = 'Get parameters',form=form))
@app.route('/evaluate/<pos_init>/<speed_init>', methods = ['GET','POST'])
def evaluate(pos_init,speed_init):
    pole_borders = np.array([[-5,5],[-5,5]], dtype=np.single)
    origin = float(pos_init)
    environment = pole.Environment(\
        pole_borders,origin,resistance=1/8,dt=1/4)
    pole1 = pole.Obstacle(pole.mountain,[np.array([1,1]),5],"first_mountain")
    pole2 = pole.Obstacle(pole.mountain,[np.array([2,-1]),8],"second_mountain")
    poles = [pole1,pole2]
    game = pole.Game(environment,poles)
    game.print_report(speed_init)
    return(render_template('parameter.html', \
        title = 'Obtain results',results_image ="foo.png" ))
