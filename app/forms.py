from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField\
    ,DecimalField, SubmitField
from wtforms.validators import DataRequired

class form_test(FlaskForm):
    position1 = DecimalField('Position 1')
    position2 = DecimalField('Position 2')
    speed_amplitude = DecimalField('Amplitude of speed')
    speed_phase = DecimalField('Phase of speed')
    submit = SubmitField('Tap OK')