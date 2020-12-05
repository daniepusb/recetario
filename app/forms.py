from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired


#
#LOGIN/SIGNUP
#
class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Password',        validators=[DataRequired()])
    submit   = SubmitField('Enviar')


#
#RECIPES
#
class RecipesForm(FlaskForm):
    title                   = StringField('Titulo de receta:',              validators=[DataRequired()])
    description             = StringField('Descripcion de receta:',         validators=[DataRequired()])
    instructions            = TextAreaField('Instrucciones de la receta:',  validators=[DataRequired()])
    ingredient__name        = StringField('Nombre del ingrediente:',        validators=[DataRequired()])
    ingredient__quantity    = StringField('Cantidad:',                      validators=[DataRequired()])
    ingredient__unit        = StringField('Unidad de medida:',              validators=[DataRequired()])
    submit                  = SubmitField('Enviar')
#
#INGREDIENTS
#
class IngredientsForm(FlaskForm):
    ingredient__name        = StringField('Nombre del ingrediente:',        validators=[DataRequired()])
    ingredient__quantity    = StringField('Cantidad:',                      validators=[DataRequired()])
    ingredient__unit        = StringField('Unidad de medida:',              validators=[DataRequired()])
    submit                  = SubmitField('Enviar')



#
#GUESTS
#
class GuestForm(FlaskForm):
    name    = StringField('Nombre:',            validators=[DataRequired()])
    email   = StringField('Correo eletronico:', validators=[DataRequired()])
    phone   = StringField('Telefono:',          validators=[DataRequired()])
    submit  = SubmitField('Enviar')


#
#INGREDIENTS
#
# """INGREDIENTS"""
# class IngredientsForm(Form): 
#     """Subform.
#     CSRF is disabled for this subform (using `Form` as parent class) because
#     it is never used by itself.
#     """
#     name    = StringField('name',       validators=[validators.InputRequired(), validators.Length(max=100)])
#     quantity= StringField('quantity',   validators=[validators.InputRequired(), validators.NumberRange(min=1)])
#     unit    = SelectField('unit',       validators=[validators.InputRequired()],    choices=[('gramos', 'gr'), ('mililitros', 'ml')] )
#     notes   = TextAreaField('notes',    validators=[validators.Length(max=255)])
#     #submit  = SubmitField('Enviar')

# class MainIngredientsForm(FlaskForm):
#     """Parent form."""
#     Ingredients = FieldList(
#         FormField(IngredientsForm),
#         min_entries=1,
#         max_entries=20
#     )
