from flask import render_template
from app import app
from app.forms import form_test

@app.route('/', methods = ['GET','POST'])
@app.route('/index')
def index():
    form = form_test()
    return(render_template('base.html',form=form))