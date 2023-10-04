from app.user.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo


class SignupForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    email = EmailField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('This Email Is Already Taken!')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This Username Is Already Taken!')


class LoginForm(FlaskForm):
    email = EmailField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if not email:
            raise ValidationError('Account with This E-mail does not Exist!')


class ResetForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    submit = SubmitField('Send Mail')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('We could not find any account with this e-mail')


class PasswordResetForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('Confirm',
                                                                             message='The passwords must match')])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Change Password')
