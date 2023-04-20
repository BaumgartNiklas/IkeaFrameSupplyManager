CREATE TABLE IF NOT EXISTS Decoration (
    ID int IDENTITY(1, 1) PRIMARY KEY,
    Name varchar(60) NOT NULL Unique,
    AmountDonated int NOT NULL,
    AmountWanted int NOT NULL,
    Priority int CHECK (Priority >= 0 AND Priority <= 2)
);