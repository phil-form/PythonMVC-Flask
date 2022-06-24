from sys import stderr


class User:
    def __init__(self, userid, username, userpassword, useremail, userdescription) -> None:
        self.userid = userid
        self.username = username
        self.userpassword = userpassword
        self.useremail = useremail
        self.userdescription = userdescription
        self.roles = []

    def isAdmin(self):
       print(self.roles, file=stderr)
       print("ADMIN" in self.roles, file=stderr)
       isAdmin = "ADMIN" in self.roles
       return isAdmin