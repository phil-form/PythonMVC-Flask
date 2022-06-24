import sys

from app import conn
from app.decorators.authRequired import authRequired
from app.models.User import User
from app.models.Role import Role

class UserRoleService:
    def findUserRoles(self, user: User):
        with conn.cursor() as cur:
            cur.execute("""
                SELECT ur.roleid, r.rolename FROM userroles ur
                JOIN roles r ON r.roleid = ur.roleid
                WHERE ur.userid = %s
            """, (user.userid,))

            roles = []

            for row in cur.fetchall():
                roles.append(str(row[1]))

            user.roles = roles

            return roles

    def userHasRole(self, roleid, user: User):
        with conn.cursor() as cur:
            cur.execute("""
                SELECT ur.roleid FROM userroles ur
                WHERE ur.userid = %s AND ur.roleid = %s
            """, (user.userid, roleid))

            if cur.rowcount == 1:
                return True
            return False

    @authRequired(level="ADMIN")
    def linkRoleToUser(self, roleid, user: User):
        if not self.userHasRole(roleid, user):
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                        INSERT INTO userroles(userid, roleid) VALUES(%s, %s) RETURNING userid
                    """, (user.userid, roleid))
                    conn.commit()
                except Exception as e:
                    print(e, file=sys.stderr)
                    conn.rollback()
                    return False

                return True

    @authRequired(level="ADMIN")
    def unlinkRoleToUser(self, roleid, user: User):
        if self.userHasRole(roleid, user) and roleid != 1:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                        DELETE FROM userroles WHERE userid = %s AND roleid = %s
                    """, (user.userid, roleid))
                    conn.commit()
                except Exception as e:
                    print(e, file=sys.stderr)
                    conn.rollback()

                    return False

                return True

        return False