from app.models.Role import Role


class User:
    def __init__(self, userid, username, userpassword, useremail, userdescription, roles) -> None:
        self.userid = userid
        self.username = username
        self.userpassword = userpassword
        self.useremail = useremail
        self.userdescription = userdescription
        self.roles = roles if roles else []

    def add_role(self, role: Role):
        if role not in self.roles:
            self.roles.append(role)

    def remove_role(self, role: Role):
        if role in self.roles:
            self.roles.remove(role)

    def has_role(self, role: Role):
        return role in self.roles

    def __str__(self):
        return f"[{self.userid}] {self.username}"
