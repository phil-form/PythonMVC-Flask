from sys import stderr
from flask import redirect, render_template, request, session, url_for
from app import app
from app.forms.UserLoginForm import UserLoginForm
from app.services.UserService import UserService
from app.forms.UserRegisterForm import UserRegisterForm
from app.forms.UserUpdateForm import UserUpdateForm

userService = UserService()


class UserController:
    @app.route('/users', methods=["GET"])
    def getUserList(self):
        users = userService.findAll()

        return render_template('users/list.html', users=users)

    @app.route('/users/<int:userid>', methods=["GET"])
    def getOneUser(self, userid: int):
        user = userService.findOne(userid)

        return render_template('users/profile.html', user=user)

    @app.route('/users/register', methods=["GET", "POST"])
    def register(self):
        form = UserRegisterForm(request.form)

        if request.method == 'POST':
            if form.validate():
                user = userService.insert(form.getAsUser())

                return redirect(url_for('getOneUser', userid=user.userid))

        return render_template('users/register.html', form=form)

    @app.route('/users/update/<int:userid>', methods=["GET", "POST"])
    def userUpdate(self, userid: int):
        form = UserUpdateForm(request.form)
        sessionUserId = session.get('userid')
        if sessionUserId is None or sessionUserId != userid:
            return redirect(url_for('index'))

        user = userService.findOne(userid)

        if request.method == 'POST':
            if form.validate():
                user = userService.update(userid, form.getAsUser(user))

                return redirect(url_for('getOneUser', userid=user.userid))

        return render_template('users/update.html', form=form, user=user, all_roles=userService.findAllRoles())

    @app.route('/login', methods=["GET", "POST"])
    def login(self):
        form = UserLoginForm(request.form)

        if request.method == 'POST':
            if form.validate():
                user = userService.login(form.getAsUser())

                if user != None:
                    session['username'] = user.username
                    session['userid'] = user.userid
                    return redirect(url_for('getOneUser', userid = user.userid))
                
                errors = {}
                errors['authentication'] = 'Wrong user or password!'

                return render_template('users/login.html', form=form, errors=errors)

        return render_template('users/login.html', form=form, errors=form.errors)

    @app.route('/logout', methods=["GET"])
    def logout(self):
        session.pop('userid', None)
        session.pop('username', None)
        return redirect(url_for('index'))

    @app.route('/profile', methods=["GET"])
    def profile(self):
        userid = session.get('userid')
        if userid != None:
            return redirect(url_for('getOneUser', userid = userid))
        else:
            return redirect(url_for('index'))