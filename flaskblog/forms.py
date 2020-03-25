from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,ValidationError
from wtforms.validators import DataRequired,Length,Email
from flaskblog.models import User

class LoginForm(FlaskForm):

    email = StringField('E-mail',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=8)])



class RegForm(FlaskForm):

    name = StringField('Name',validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=8)])

    def validate_email(self,email):

        user = User.query.filter_by(email=email.data).first()

        if user:
            raise  ValidationError('This Email has been taken Already.')