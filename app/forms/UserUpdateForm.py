from app.models.User import User
from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, StringField
from wtforms.validators import DataRequired, EqualTo


class UserUpdateForm(FlaskForm):
    # username = StringField('username', validators=[DataRequired()])
    # userpassword = StringField('userpassword', validators=[DataRequired(), EqualTo('confirm', message='passwords must match!')])
    # confirm = StringField('confirm', validators=[DataRequired()])
    useremail = StringField('useremail', validators=[DataRequired()])
    userdescription = StringField(
        'userdescription', validators=[DataRequired()])
    isAdmin = BooleanField('isAdmin', validators=[])

    def getAsUser(self, user: User) -> User:
        user.useremail = self.useremail.data
        user.userdescription = self.userdescription.data

        if self.admin_role:
            # FIXME this is not okay... use an enum ?
            user.add_role(Role(1, "ADMIN"))
        if self.user_role:
            user.add_role(Role(2, "USER"))  # FIXME same

        return user
