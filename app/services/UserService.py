from sys import stderr

from flask import session
from app.forms.UserUpdateForm import UserUpdateForm
from app.models.User import User
from app.services.IService import IService
from app import conn
import bcrypt

from app.services.UserRoleService import UserRoleService

class UserService(IService):
    def __init__(self) -> None:
        self.userRoleService = UserRoleService()

    def login(self, user: User):
        toLogin = self.findOneBy(username=user.username)

        if toLogin != None and bcrypt.checkpw(user.userpassword.encode('utf-8'), toLogin.userpassword.encode('utf-8')):
            return toLogin

        return None

    def findAll(self):
        with conn.cursor() as cur:
            cur.execute("SELECT userid, username, useremail, userdescription FROM users")

            users = []

            for user in cur.fetchall():
                users.append(User(user[0], user[1], '', user[2], user[3]))

            return users

    def findOne(self, dataId: int):
        with conn.cursor() as cur:
            cur.execute("SELECT userid, username, useremail, userdescription FROM users WHERE userid = %s", (dataId,))

            userData = cur.fetchone()
            if cur.rowcount == 1:
                user = User(userData[0], userData[1], '', userData[2], userData[3])
                user.roles = self.userRoleService.findUserRoles(user)
                return user
            
            return None

    def findOneBy(self, **kwargs):
        with conn.cursor() as cur:
            query = "SELECT userid, username, userpassword, useremail, userdescription FROM users"
            values = []
            firstItem = True
            for key, val in kwargs.items():
                query += " WHERE " if firstItem else " AND "
                query += f"{key} = %s"
                values.append(val)
                firstItem = False

            cur.execute(query, values)

            userData = cur.fetchone()

            if cur.rowcount == 1:
                return User(userData[0], userData[1], userData[2], userData[3], userData[4])
            
            return None

    def insert(self, data: User):
        with conn.cursor() as cur:
            try:
                password = data.userpassword.encode('utf-8')
                mySalt = bcrypt.gensalt()
                hashPassword = bcrypt.hashpw(password, mySalt).decode('utf-8')

                cur.execute("INSERT INTO users(username, userpassword, useremail, userdescription) VALUES (%s, %s, %s, %s) RETURNING userid", 
                    (data.username, hashPassword, data.useremail, data.userdescription))

                data.userid = cur.fetchone()[0]
                self.userRoleService.linkRoleToUser(1, data)

                conn.commit()

                return data
            except Exception as e:
                print(e, file=stderr)
                conn.rollback()

            return None

    def update(self, dataId: int, data: UserUpdateForm):
        user = self.findOne(dataId)

        if user == None:
            return None

        user = data.getAsUser(user)

        with conn.cursor() as cur:
            try:
                cur.execute("UPDATE users SET useremail = %s, userdescription = %s WHERE userid = %s", 
                    (user.useremail, user.userdescription, dataId))

                if data.isAdmin.data:
                    self.userRoleService.linkRoleToUser(2, user)
                elif "ADMIN" in user.roles:
                    self.userRoleService.unlinkRoleToUser(2, user)

                print(dataId, file=stderr)
                print(session.get('userid'), file=stderr)
                if dataId == session.get('userid'):
                    roles = self.userRoleService.findUserRoles(user)
                    print(roles, file=stderr)
                    session['userroles'] = roles
                    user.roles = roles

                conn.commit()

                return user
            except Exception as e:
                print(e, file=stderr)
                conn.rollback()

            return None
    
    def delete(self, dataId: int):
        with conn.cursor() as cur:
            try:
                cur.execute("DELETE FROM userroles WHERE userid = %s", (dataId,))
                cur.execute("DELETE FROM users WHERE userid = %s", 
                    (dataId,))
                conn.commit()

                return dataId
            except Exception as e:
                print(e, file=stderr)
                conn.rollback()

            return None