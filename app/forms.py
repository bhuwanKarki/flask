from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired,Email,EqualTo,ValidationError
from app.models import User
from wtforms import TextAreaField
from wtforms.validators import Length

class LoginForm(FlaskForm):
    username=StringField("Username",validators=[DataRequired()])
    password=StringField("Password",validators=[DataRequired()])
    remember_me=BooleanField("Remember me")
    submit=SubmitField("SignIn")
    
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("please use different username")

    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("please use different email address")

    
class EditProfile_form(FlaskForm):
    username=StringField('username',validators=[DataRequired()])
    about_me=TextAreaField("About me",validators=[Length(min=0,max=140)])
    submit=SubmitField("Submit")
    
    def __init__(self,original_username,*args,**kwargs):
        super(EditProfile_form,self).__init__(*args,**kwargs)
        self.original_username=original_username
    def validate_username(self,username):
        if username.data !=self.original_username:
            user=User.query.filter(username=self.username.data).first()
            if user is not None:
                raise ValidationError("Please use a different username")
    
    
class EmptyForm(FlaskForm):
    submit=SubmitField("submit")
    
class PostForm(FlaskForm):
    post=TextAreaField("say something",validators=[DataRequired(),Length(min=1,max=140)])
    submit=SubmitField("submit")
    
class ResetPasswordRequestForm(FlaskForm):
    email=StringField("Email",validators=[DataRequired(),Email()])
    submit=SubmitField("Request Password Reset")

class ResetPasswordForm(FlaskForm):
    password=PasswordField("password",validators=[DataRequired()])
    password2=PasswordField("repeat Password",validators=[DataRequired(),EqualTo("password")])
    submit=SubmitField("Request Password Request")