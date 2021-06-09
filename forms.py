from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.fields.html5 import EmailField
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,IntegerField,SubmitField


from flask_login import current_user
from models import User

class LoginForm(FlaskForm):
    username = StringField('UserName',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    username = StringField('UserName',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('pass_confirm',message='Passwords must match!')])
    pass_confirm = PasswordField('Confirm Password',validators=[DataRequired()])
    submit = SubmitField('Register!')

    def check_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def check_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Your username has been registered already!')


class UpdateUserForm(FlaskForm):


    username = StringField('UserName',validators=[DataRequired()])
    submit = SubmitField('Update')

    def check_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Your username has been registered already!')


class AddEntryForm(FlaskForm):
    category = StringField('Category',validators=[DataRequired()])
    sitename = StringField('Name',validators=[DataRequired()])
    u_name = StringField('username',validators=[DataRequired()])
    u_pwd = StringField('password', validators=[DataRequired()])
    submit = SubmitField("Post")
