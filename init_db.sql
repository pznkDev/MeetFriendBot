CREATE USER meet_user WITH password 'meet_password';
GRANT ALL ON database meet_db TO meet_user;


CREATE TABLE states (
   id serial PRIMARY KEY,
   chat_id int UNIQUE NOT NULL,
   state varchar(50),
   age int,
   sex varchar(6),
   location json,
   time int
);
ALTER TABLE states OWNER TO meet_user;

CREATE TABLE users (
   id serial PRIMARY KEY,
   chat_id int UNIQUE NOT NULL,
   username varchar(50) UNIQUE NOT NULL,
   age varchar(50) NOT NULL,
   sex varchar(6),
   location json,
   expires_at TIMESTAMP DEFAULT now()
);
ALTER TABLE users OWNER TO meet_user;
