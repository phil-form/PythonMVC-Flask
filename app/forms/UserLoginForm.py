from flask_wtf import FlaskForm
from wtforms import StringField, EmailField
from wtforms.validators import DataRequired, EqualTo
from app.models.User import User

class UserLoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    userpassword = StringField('userpassword', validators=[DataRequired()])

    def getAsUser(self) -> User:
        return User(0, self.username.data, self.userpassword.data, '', '')