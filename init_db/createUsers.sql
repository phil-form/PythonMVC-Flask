CREATE TABLE users(
    userid SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    userpassword VARCHAR(255) NOT NULL,
    useremail VARCHAR(255) UNIQUE NOT NULL,
    userdescription VARCHAR(255)
);

CREATE INDEX username_index ON users(username);
CREATE INDEX useremail_index ON users(useremail);


CREATE TABLE roles(
    roleid SERIAL PRIMARY KEY,
    rolename VARCHAR(30) NOT NULL
);

CREATE TABLE usersroles(
    userid integer NOT NULL,
    roleid integer NOT NULL,
    CONSTRAINT contacts-roles_pkey PRIMARY KEY (userid)
        INCLUDE(roleid),
    CONSTRAINT users_fkey FOREIGN KEY (userid)
        REFERENCES public.users (userid) MATCH SIMPLE,
    CONSTRAINT roles_fkey FOREIGN KEY (roleid)
        REFERENCES public.roles (roleid) MATCH SIMPLE
);