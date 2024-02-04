CREATE TABLE courts (
	CourtNumber INT NOT NULL,
	Type TEXT,
	IsOutdoor DEFAULT 0,
	PRIMARY KEY (CourtNumber)
);

-- One to many
CREATE TABLE free_courts (
	CourtNumber INT NOT NULL,
	Date TEXT NOT NULL,
	Time TEXT NOT NULL,
	CONSTRAINT PK_free_courts PRIMARY KEY (CourtNumber, Date, Time),
	FOREIGN KEY (CourtNumber) REFERENCES courts(CourtNumber)
);
