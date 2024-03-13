from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, PasswordField, DateField,
                      TextAreaField, RadioField, SelectMultipleField , MultipleFileField, BooleanField)

from wtforms.validators import DataRequired, URL, Email, InputRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_uploads import UploadSet, IMAGES 

images = UploadSet('images', IMAGES)

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


