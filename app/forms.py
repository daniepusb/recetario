from flask_wtf import FlaskForm
from wtforms.fields import HiddenField, StringField, IntegerField, PasswordField, SubmitField, TextAreaField, SelectField, FormField, FieldList
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
class RecipeIngredientsForm(FlaskForm):
    name        = StringField('Nombre del ingrediente:')
    quantity    = IntegerField('Cantidad:')
    unit        = StringField('Unidad de medida:')

#
#RECIPES (NOT USE BUT STILL UPDATED)
#
class RecipesForm(FlaskForm):
    title                   = StringField('Titulo de receta:',              validators=[DataRequired()])
    description             = StringField('Descripcion de receta:',         validators=[DataRequired()])
    instructions            = TextAreaField('Instrucciones de la receta:',  validators=[DataRequired()])
    servings                = IntegerField('Cantidad de porciones:',        validators=[DataRequired()])
    #ingredients             = FormField(IngredientsForm)
    submit                  = SubmitField('Enviar')


#
#INGREDIENT 
#
class IngredientForm(FlaskForm):
    is_gluten_free  = StringField('Libre de Gluten')
    quantity        = IntegerField('Cantidad:')
    unit            = StringField('Unidad de medida:')
    price           = IntegerField('Costo')



#
#GUESTS
#
class GuestForm(FlaskForm):
    name    = StringField('Nombre:',            validators=[DataRequired()])
    email   = StringField('Correo electrónico:',validators=[DataRequired()])
    phone   = StringField('Telefono:',          validators=[DataRequired()])
    submit  = SubmitField('Enviar')
