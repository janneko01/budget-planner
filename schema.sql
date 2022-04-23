CREATE TABLE user (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT
);

CREATE TABLE monthlyMoney (
    id SERIAL PRIMARY KEY,
    unused INTEGER,
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