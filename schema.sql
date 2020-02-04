-- original example from: https://flask.palletsprojects.com/en/1.1.x/tutorial/database/#create-the-tables
-- and modified to fit the data model I derived for this exercise

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS message;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE message (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  sender_id INTEGER NOT NULL,
  recipient_id INTEGER NOT NULL,
  content TEXT NOT NULL,
  creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (sender_id) REFERENCES user (id)
  FOREIGN KEY (recipient_id) REFERENCES user (id)
);