from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, DecimalField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Password',        validators=[DataRequired()])
    submit   = SubmitField('Enviar')

class RecipesForm(FlaskForm):
    title       = StringField('Titulo de receta:',      validators=[DataRequired()])
    description = StringField('Descripcion de receta:', validators=[DataRequired()])
    submit      = SubmitField('Enviar')

class GuestForm(FlaskForm):
    name    = StringField('Nombre:',            validators=[DataRequired()])
    email   = StringField('Correo eletronico:', validators=[DataRequired()])
    phone   = StringField('Telefono:',          validators=[DataRequired()])
    submit  = SubmitField('Enviar')
