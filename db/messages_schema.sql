-- original example from: https://www.sqlitetutorial.net/sqlite-python/create-tables/
-- and modified to fit the data model I derived for this exercise

PRAGMA foreign_keys = ON; -- FKs are not enabled by default

DROP TABLE IF EXISTS messages;

CREATE TABLE messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  sender_id INTEGER NOT NULL,
  recipient_id INTEGER NOT NULL,
  content TEXT NOT NULL,
  creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (sender_id) REFERENCES users(id),
  FOREIGN KEY (recipient_id) REFERENCES users(id)
);