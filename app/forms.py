from flask_wtf import FlaskForm
from wtforms.fields import HiddenField, StringField, PasswordField, SubmitField, TextAreaField, SelectField, FormField, FieldList
from wtforms.validators import DataRequired


#
#LOGIN/SIGNUP
#
class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Password',        validators=[DataRequired()])
    submit   = SubmitField('Enviar')


#
#INGREDIENTS (NOT USE)
#
class IngredientsForm(FlaskForm):
    name        = StringField('Nombre del ingrediente:')
    quantity    = StringField('Cantidad:')
    unit        = StringField('Unidad de medida:')
#
#RECIPES (NOT USE)
#
class RecipesForm(FlaskForm):
    title                   = StringField('Titulo de receta:',              validators=[DataRequired()])
    description             = StringField('Descripcion de receta:',         validators=[DataRequired()])
    instructions            = TextAreaField('Instrucciones de la receta:',  validators=[DataRequired()])
    ingredients             = FormField(IngredientsForm)
    submit                  = SubmitField('Enviar')


#
#GUESTS
#
class GuestForm(FlaskForm):
    name    = StringField('Nombre:',            validators=[DataRequired()])
    email   = StringField('Correo eletronico:', validators=[DataRequired()])
    phone   = StringField('Telefono:',          validators=[DataRequired()])
    submit  = SubmitField('Enviar')
