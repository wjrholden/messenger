-- original example from: https://www.sqlitetutorial.net/sqlite-python/create-tables/
-- and modified to fit the data model I derived for this exercise

DROP TABLE IF EXISTS users;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);