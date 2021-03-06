from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


# Clase para los login
class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[
                           DataRequired()])  # Validar los datos
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Ingresar')


class TodoForm(FlaskForm):
    description = StringField('Descripción', validators=[DataRequired()])
    submit = SubmitField('Agregar')

class DeleteTodoForm(FlaskForm):
    submit = SubmitField()


class UpdateTodoForm(FlaskForm):
    submit = SubmitField()
