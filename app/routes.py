from flask import render_template, flash, redirect, url_for,request, session
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
        session['pos_init'] = [request.form['position1'],\
            request.form['position2']]
        session['speed_init'] = [request.form['speed_amplitude'],\
            request.form['speed_phase']]
        return redirect(url_for('evaluate'))
    return(render_template('parameter.html', \
        title = 'Get parameters',form=form))
@app.route('/evaluate', methods = ['GET','POST'])
def evaluate():
    pole_borders = np.array([[-5,5],[-5,5]], dtype=np.single)
    origin = np.array(session['pos_init'],dtype=np.single)
    user_input = np.array(session['speed_init'],dtype=np.single)
    environment = pole.Environment(\
        pole_borders,origin,resistance=1/8,dt=1/4)
    pole1 = pole.Obstacle(pole.mountain,[np.array([1,1]),5],"first_mountain")
    pole2 = pole.Obstacle(pole.mountain,[np.array([2,-1]),8],"second_mountain")
    poles = [pole1,pole2]
    game = pole.Game(environment,poles)
    game.print_report(user_input)
    return(render_template('evaluate.html', \
        title = 'Obtain results',results_image ="foo.png" ))
