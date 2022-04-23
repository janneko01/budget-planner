CREATE TABLE user (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT
);

CREATE TABLE monthlyMoney (
    id SERIAL PRIMARY KEY,
    unused INTEGER
);

CREATE TABLE costs (
    id SERIAL PRIMARY KEY,
    eventTime DATETIME,
    category TEXT,
    product TEXT,
    price INTEGER
);