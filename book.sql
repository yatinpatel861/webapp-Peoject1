 CREATE TABLE Book(
    id SERIAL PRIMARY KEY,
    isbn VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year Integer NOT NULLcre
);


CREATE TABLE review(
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES registration(id),
    book_id INTEGER REFERENCES book(id),
    reviewtext VARCHAR,
    rating INTEGER NOT NULL,
    date timestamp NOT NULL DEFAULT NOW()
);