from sys import stderr
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
                users.append(User(user[0], user[1], '', user[2], user[3]))

            return users

    def findOne(self, dataId: int):
        with conn.cursor() as cur:
            cur.execute("SELECT userid, username, useremail, userdescription FROM users WHERE userid = %s", (dataId,))

            userData = cur.fetchone()
            if cur.rowcount == 1:
                return User(userData[0], userData[1], '', userData[2], userData[3])
            
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
                conn.commit()

                data.userid = cur.fetchone()[0]

                return data
            except Exception as e:
                print(e, file=stderr)
                conn.rollback()

            return None

    def update(self, dataId: int, data):
        with conn.cursor() as cur:
            try:
                cur.execute("UPDATE users SET useremail = %s, userdescription = %s WHERE userid = %s", 
                    (data.useremail, data.userdescription, dataId))
                conn.commit()

                return data
            except Exception as e:
                print(e, file=stderr)
                conn.rollback()

            return None

    def delete(self, dataId: int):
        with conn.cursor() as cur:
            try:
                cur.execute("DELETE FROM users WHERE userid = %s", 
                    (dataId,))
                conn.commit()

                return dataId
            except Exception as e:
                print(e, file=stderr)
                conn.rollback()

            return None