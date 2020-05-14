 DROP TABLE IF EXISTS post;
 CREATE TABLE post (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   title TEXT NOT NULL,
   'text' TEXT NOT NULL,
   Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
 );

DROP TABLE IF EXISTS users;
 CREATE TABLE users (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   username TEXT NOT NULL UNIQUE,
   pword TEXT NOT NULL,
   salt TEXT NOT NULL

 );

-- -- pword = default (hashed)
-- INSERT INTO users(username, pword, salt) VALUES('admin', '$2b$12$UmuWa4uOCvs4Gcn8t5SMJOQqPdl8hHM1XUAEdSXMm8JAScPVxnK2O', '$2b$12$UmuWa4uOCvs4Gcn8t5SMJO');