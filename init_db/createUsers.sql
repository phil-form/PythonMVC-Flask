CREATE TABLE users(
    userid SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    userpassword VARCHAR(255) NOT NULL,
    useremail VARCHAR(255) UNIQUE NOT NULL,
    userdescription VARCHAR(255)
);

CREATE INDEX username_index ON users(username);
CREATE INDEX useremail_index ON users(useremail);