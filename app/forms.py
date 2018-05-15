from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User
from flask_babel import lazy_gettext as _l
from flask_babel import _

# Form for login
class LoginForm(FlaskForm):
    username = StringField(_l('UserName'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))

# Form to support new user registration
# WTForms automatically uses custom validators
# when named "validate_<field>"
class RegistrationForm(FlaskForm):
    username = StringField(_l('UserName'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Confirm Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Register'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_('Please choose a different username.'))
    
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_('Email address already in use.'))

# Form to allow users to edit profile
class EditProfileForm(FlaskForm):
    username = StringField(_l('UserName'), validators=[DataRequired()])
    about_me = TextAreaField(_l('About Me'), validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('Submit'))

    # Overloaded constructor to add original_username
    # to the EditProfileForm object
    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
    
    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Please provide a different username.'))

# Blog entry submission form
class PostForm(FlaskForm):
    post = TextAreaField(_l('Say something'), validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField(_l('Submit'))

# Reset password email form
class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators = [DataRequired(), Email()])
    submit = SubmitField(_l('Request Password Reset'))

# Reset password entry form
class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(_l('Repeat Password'), 
        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Reset Password'))