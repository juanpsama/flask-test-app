from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, PasswordField, DateField,
                      TextAreaField, MultipleFileField)
from wtforms.validators import DataRequired, InputRequired

class loginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class DocumentForm(FlaskForm):
    name = StringField('Nombre del archivo: ', validators=[DataRequired()])
    folio = StringField('Folio: ', validators=[DataRequired()])
    description = TextAreaField('Descripcion: ', validators=[DataRequired()])

    date = DateField('Fecha de expedicion: ', validators= [DataRequired()])
    
    file = MultipleFileField('Factura', validators=[
        InputRequired()
    ])
    submit = SubmitField('Subir')


