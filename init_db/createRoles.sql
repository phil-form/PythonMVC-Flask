CREATE TABLE roles(
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE NOT NULL
);
CREATE INDEX role_index ON roles(role_name);

CREATE TABLE users_x_roles(
    role_id SERIAL NOT NULL,
    userid SERIAL NOT NULL,
    CONSTRAINT fk_role_user_rid FOREIGN KEY (role_id) REFERENCES roles(role_id),
    CONSTRAINT fk_role_user_uid FOREIGN KEY (userid) REFERENCES users(userid),
    UNIQUE(role_id, userid)
);

INSERT INTO roles(role_name) VALUES ('ADMIN');
INSERT INTO roles(role_name) VALUES ('USER');

