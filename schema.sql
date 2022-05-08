CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT
);

CREATE TABLE income (
    id SERIAL PRIMARY KEY,
    eventDate DATE,
    source Text,
    income INTEGER,
    userid INTEGER
);

CREATE TABLE costs (
    id SERIAL PRIMARY KEY,
    eventDate DATE,
    category TEXT,
    product TEXT,
    price INTEGER,
    userid INTEGER
);

CREATE TABLE userSettings (
    id SERIAL PRIMARY KEY,
    targetBudget INTEGER,
    userid INTEGER
);