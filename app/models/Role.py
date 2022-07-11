

class Role:
    def __init__(self, role_id, role_name):
        self.__role_id = role_id
        self.__role_name = role_name

    @property
    def role_id(self):
        return self.__role_id

    @property
    def role_name(self):
        return self.__role_name

    def __str__(self):
        return self.role_name

    def __eq__(self, other):
        return self.role_id == other.role_id
