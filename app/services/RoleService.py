from sys import stderr
from app.models.Role import Role
from app.services.IService import IService
from app import conn

class RoleService(IService):
    def findAll(self):
        with conn.cursor() as cur:
            cur.execute("SELECT roleid, rolename FROM roles")

            roles = []

            for role in cur.fetchall():
                roles.append(Role(role[0], role[1]))

            return roles

    def findOne(self, roleId: int):
        with conn.cursor() as cur:
            cur.execute("SELECT roleid, rolename FROM roles WHERE roleid = %s", (roleId,))

            roleData = cur.fetchone()
            if cur.rowcount == 1:
                return Role(role[0], role[1])
            
            return None

    def findOneBy(self, **kwargs):
        pass

    def insert(self, role: Role):
        pass

    def update(self, roleId: int, data):
        pass

    def delete(self, roleId: int):
        with conn.cursor() as cur:
            try:
                cur.execute("DELETE FROM roles WHERE roleid = %s", 
                    (roleId,))
                conn.commit()

                return roleId
            except Exception as e:
                print(e, file=stderr)
                conn.rollback()

            return None