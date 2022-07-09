from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField\
    ,BooleanField, SubmitField
from wtforms.validators import DataRequired

class form_test(FlaskForm):
    position1 = StringField('Position 1')
    submit = SubmitField('Tap OK')