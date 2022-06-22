from flask_wtf import FlaskForm
from wtforms import StringField, EmailField
from wtforms.validators import DataRequired, EqualTo
from app.models.User import User

class UserRegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    userpassword = StringField('userpassword', validators=[DataRequired(), EqualTo('confirm', message='passwords must match!')])
    confirm = StringField('confirm', validators=[DataRequired()])
    useremail = StringField('useremail', validators=[DataRequired()])
    userdescription = StringField('userdescription', validators=[DataRequired()])

    def getAsUser(self) -> User:
        return User(0, self.username.data, self.userpassword.data, self.useremail.data, self.userdescription.data)