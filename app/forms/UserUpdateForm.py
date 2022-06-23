from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

from app.models.Role import Role
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

        if self.admin_role:
            user.add_role(Role(1, "ADMIN")) # FIXME this is not okay... use an enum ?
        if self.user_role:
            user.add_role(Role(2, "USER")) # FIXME same

        return user
