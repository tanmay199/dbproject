CREATE TABLE train(
    trainID INTEGER NOT NULL PRIMARY KEY,
    startpoint VARCHAR(20) NOT NULL,
    endpoint VARCHAR(20) NOT NULL
);

CREATE TABLE schedule(
    trainID INTEGER NOT NULL,
    dateofjourney DATE NOT NULL,
    AC INTEGER NOT NULL,
    nonAC INTEGER NOT NULL,
    PRIMARY KEY (trainID, dateofjourney),
    FOREIGN KEY(trainID) REFERENCES train(trainID)
);

CREATE TABLE userrecord(
    id serial PRIMARY KEY,
    firstname VARCHAR(20) NOT NULL,
    lastname VARCHAR(20),
    credit_card VARCHAR(20) NOT NULL,
    password text,
    address text
);

CREATE TABLE ticket(
    PNR CHAR(10) NOT NULL PRIMARY KEY,
    dateofjourney DATE NOT NULL,
    trainID INTEGER NOT NULL,
    user_id int NOT NULL,
    FOREIGN KEY(user_id) REFERENCES userrecord(id), 
    FOREIGN KEY(trainID) REFERENCES train(trainID)
);

CREATE TABLE ticketdetail(
    PNR CHAR(10) NOT NULL, 
    firstname VARCHAR(20) NOT NULL,
    lastname VARCHAR(20), 
    age INTEGER NOT NULL,
    gender VARCHAR(10) NOT NULL,
    berth VARCHAR(5),
    FOREIGN KEY(PNR) REFERENCES ticket(PNR)
);

