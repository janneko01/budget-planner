CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT
);

CREATE TABLE income (
    id SERIAL PRIMARY KEY,
    eventTime TIMESTAMP,
    money INTEGER,
    userid INTEGER
);

CREATE TABLE costs (
    id SERIAL PRIMARY KEY,
    eventTime TIMESTAMP,
    category TEXT,
    product TEXT,
    price INTEGER,
    userid INTEGER
);