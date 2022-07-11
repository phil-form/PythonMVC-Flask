from sys import stderr

from app.models.Role import Role
from app.models.User import User
from app.services.IService import IService
from app import conn
import bcrypt


class UserService(IService):
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
                users.append(User(user[0], user[1], '', user[2], user[3], roles=self.findUserRoles(user[0])))

            return users

    def findOne(self, dataId: int):
        with conn.cursor() as cur:
            cur.execute("SELECT userid, username, useremail, userdescription FROM users WHERE userid = %s", (dataId,))

            userData = cur.fetchone()
            if cur.rowcount == 1:
                return User(userData[0], userData[1], '', userData[2], userData[3], roles=self.findUserRoles(userData[0]))

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
                return User(userData[0], userData[1], userData[2], userData[3], userData[4], roles=self.findUserRoles(userData[0]))

            return None

    def insert(self, data: User):
        print(data)
        with conn.cursor() as cur:
            try:
                inserted_user = self.__insertUser(data)

                if len(data.roles) == 0:
                    data.add_role(self.findRoleBy(role_name="USER"))
                for role in data.roles:
                    self.__insertRoleToUser(data.userid, role.role_id)

                conn.commit()
                return inserted_user
            except Exception as e:
                print(e, file=stderr)
                conn.rollback()

            return None

    def __insertUser(self, data: User):
        with conn.cursor() as cur:
            password = data.userpassword.encode('utf-8')
            mySalt = bcrypt.gensalt()
            hashPassword = bcrypt.hashpw(password, mySalt).decode('utf-8')

            cur.execute(
                "INSERT INTO users(username, userpassword, useremail, userdescription) VALUES (%s, %s, %s, %s) RETURNING userid",
                (data.username, hashPassword, data.useremail, data.userdescription))

            # we don't want to commit before user AND roles are successfully inserted
            # conn.commit()

            data.userid = cur.fetchone()[0]

            return data

    def __insertRoleToUser(self, userid, role_id):
        with conn.cursor() as cur:
            cur.execute("INSERT INTO users_x_roles(userid, role_id) VALUES (%s, %s)",
                            (userid, role_id))

    def update(self, dataId: int, data: User):
        with conn.cursor() as cur:
            try:
                cur.execute("UPDATE users SET useremail = %s, userdescription = %s WHERE userid = %s",
                            (data.useremail, data.userdescription, dataId))

                known_roles = self.findUserRoles(data.userid)
                for role in data.roles:
                    if role not in known_roles:
                        self.__insertRoleToUser(data.userid, role.role_id)
                for role in known_roles:
                    if role not in data.roles:
                        self.__deleteRoleFromUser(data.userid, role.role_id)

                conn.commit()
                return data

            except Exception as e:
                print(e, file=stderr)
                conn.rollback()

            return None

    def delete(self, dataId: int):
        with conn.cursor() as cur:
            try:
                cur.execute("DELETE FROM users_x_roles WHERE userid = %s",
                            (dataId,))
                cur.execute("DELETE FROM users WHERE userid = %s",
                            (dataId,))
                conn.commit()

                return dataId
            except Exception as e:
                print(e, file=stderr)
                conn.rollback()

            return None

    def __deleteRoleFromUser(self, userid, role_id):
        with conn.cursor() as cur:
            try:
                cur.execute("DELETE FROM users_x_roles WHERE userid = %s AND role_id = %s",
                            (userid, role_id))
                conn.commit()

            except Exception as e:
                print(e, file=stderr)
                conn.rollback()

            return None

    def findAllRoles(self):
        with conn.cursor() as cur:
            cur.execute("SELECT role_id, role_name FROM roles")
            roles = []
            for role in cur.fetchall():
                roles.append(Role(role[0], role[1]))
            return roles

    def findUserRoles(self, userid):
        with conn.cursor() as cur:
            try:
                cur.execute("SELECT role_id, userid FROM users_x_roles WHERE userid = %s", (str(userid),))
                roles = []
                for role in cur.fetchall():
                    roles.append(self.findRoleBy(role_id=role[0]))
                return roles

            except Exception as e:
                print(e, file=stderr)
                conn.rollback()
            return None

    def findRoleBy(self, **kwargs) -> Role:
        with conn.cursor() as cur:
            try:
                query = "SELECT role_id, role_name FROM roles"
                values = []
                first_item = True
                for key, val in kwargs.items():
                    query += " WHERE " if first_item else " AND "
                    query += f"{key} = %s"
                    values.append(val)
                    first_item = False

                cur.execute(query, values)
                role = cur.fetchone()
                return Role(role[0], role[1])

            except Exception as e:
                print(e, file=stderr)
                conn.rollback()
            return None
