from flask_wtf import FlaskForm
from wtforms import StringField, EmailField
from wtforms.validators import DataRequired, EqualTo
from app.models.User import User

class UserUpdateForm(FlaskForm):
    # username = StringField('username', validators=[DataRequired()])
    # userpassword = StringField('userpassword', validators=[DataRequired(), EqualTo('confirm', message='passwords must match!')])
    # confirm = StringField('confirm', validators=[DataRequired()])
    useremail = StringField('useremail', validators=[DataRequired()])
    userdescription = StringField('userdescription', validators=[DataRequired()])

    def getAsUser(self, user: User) -> User:
        user.useremail = self.useremail.data
        user.userdescription = self.userdescription.data

        return user