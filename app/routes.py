from flask import render_template, flash, redirect
from app import app
from app.forms import form_test

@app.route('/', methods = ['GET','POST'])
@app.route('/index', methods = ['GET','POST'])
def index():
    form = form_test()
    if form.validate_on_submit():
        flash('Position vector: ({},{}),\
            vector initial speed: ({},{})'\
                .format(form.position1.data,form.position2.data\
                    ,form.speed_amplitude.data,form.speed_phase.data))
        return redirect('/index')
    return(render_template('base.html', \
        title = 'Get parameters',form=form))