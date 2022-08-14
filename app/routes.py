from flask import render_template, flash, redirect, url_for,request, session
from app import app
from app.forms import form_test
import numpy as np
import matplotlib.pyplot as plt
import pole
from config import Config

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
    origin = np.array(session['pos_init'],dtype=np.single)
    user_input = np.array(session['speed_init'],dtype=np.single)
    environment = pole.Environment(\
        Config.pole_borders,Config.targets,\
            origin, resistance=Config.resistance,\
                dt=Config.dt)
    game = pole.Game(environment,\
        Config.poles)
    time,hist_pos,pos,speed = game.path_simulation(user_input)       
    game.take_a_snapshot(hist_pos)
    return(render_template('evaluate.html', \
        title = 'Obtain results',results_image ="foo.gif" ))
