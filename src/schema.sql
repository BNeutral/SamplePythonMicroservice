DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS ars_balances;
DROP TABLE IF EXISTS usdt_balances;
DROP TABLE IF EXISTS btc_balances;


CREATE TABLE users (
  uuid INTEGER PRIMARY KEY UNIQUE NOT NULL, -- Don't use autoincrement ints for privacy/security reasons.
  names TEXT NOT NULL,
  surnames TEXT NOT NULL,
  alias TEXT UNIQUE NOT NULL,
  email TEXT UNIQUE NOT NULL
  -- passwordhash BLOB NOT NULL -- Not needed for this exercise.
);

CREATE TABLE ars_balances (
  uuid INTEGER PRIMARY KEY NOT NULL,
  balance INTEGER NOT NULL CHECK (balance >= 0),
  FOREIGN KEY(uuid) REFERENCES users(uuid)
);

CREATE TABLE usdt_balances (
  uuid INTEGER PRIMARY KEY NOT NULL,
  balance INTEGER NOT NULL CHECK (balance >= 0),
  FOREIGN KEY(uuid) REFERENCES users(uuid)
);

CREATE TABLE btc_balances (
  uuid INTEGER PRIMARY KEY NOT NULL,
  balance INTEGER NOT NULL CHECK (balance >= 0),
  FOREIGN KEY(uuid) REFERENCES users(uuid)
);

CREATE TABLE transactions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  uuid INTEGER NOT NULL,
  timestamp INTEGER NOT NULL,
  operation INTEGER NOT NULL,
  currency INTEGER NOT NULL,
  amount INTEGER NOT NULL,
  FOREIGN KEY(uuid) REFERENCES users(uuid)
);