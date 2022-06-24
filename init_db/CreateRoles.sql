CREATE TABLE roles(
    roleid SERIAL PRIMARY KEY,
    rolename VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE userroles(
    roleid INT NOT NULL,
    userid INT NOT NULL,
    CONSTRAINT fk_userroles_rid FOREIGN KEY (roleid) REFERENCES roles(roleid),
    CONSTRAINT fk_userroles_uid FOREIGN KEY (userid) REFERENCES users(userid),
    UNIQUE(roleid, userid)
);