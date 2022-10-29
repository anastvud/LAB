CREATE TABLE `City` (
	idcity INTEGER NOT NULL AUTO_INCREMENT,
	name VARCHAR(15),
	country VARCHAR(15),
	PRIMARY KEY (idcity)
);

CREATE TABLE `User` (
	iduser INTEGER NOT NULL AUTO_INCREMENT,
	name VARCHAR(15),
	surname VARCHAR(15),
	passport VARCHAR(10),
	username VARCHAR(20),
	password VARCHAR(20),
	PRIMARY KEY (iduser)
);

CREATE TABLE `Transport` (
	idtransport INTEGER NOT NULL AUTO_INCREMENT,
	name VARCHAR(15),
	PRIMARY KEY (idtransport)
);

CREATE TABLE `Hotel` (
	idhotel INTEGER NOT NULL AUTO_INCREMENT,
	name VARCHAR(15),
	PRIMARY KEY (idhotel)
);

CREATE TABLE `Payment` (
	idpayment INTEGER NOT NULL AUTO_INCREMENT,
	name VARCHAR(15),
	PRIMARY KEY (idpayment)
);

CREATE TABLE `Trip` (
	idtrip INTEGER NOT NULL AUTO_INCREMENT,
	days INTEGER,
	start_date DATE,
	transport_id INTEGER,
	PRIMARY KEY (idtrip),
	FOREIGN KEY(transport_id) REFERENCES `Transport` (idtransport)
);

CREATE TABLE `HotelsChoice` (
	idchoice INTEGER NOT NULL AUTO_INCREMENT,
	hotel_id INTEGER,
	city_id INTEGER,
	PRIMARY KEY (idchoice),
	FOREIGN KEY(hotel_id) REFERENCES `Hotel` (idhotel),
	FOREIGN KEY(city_id) REFERENCES `City` (idcity)
);

CREATE TABLE `Booking` (
	idbooking INTEGER NOT NULL AUTO_INCREMENT,
	client_id INTEGER,
	trip_id INTEGER,
	payment_id INTEGER,
	PRIMARY KEY (idbooking),
	FOREIGN KEY(client_id) REFERENCES `User` (iduser),
	FOREIGN KEY(trip_id) REFERENCES `Trip` (idtrip),
	FOREIGN KEY(payment_id) REFERENCES `Payment` (idpayment)
);

CREATE TABLE `Stop` (
	idstop INTEGER NOT NULL AUTO_INCREMENT,
	trip_id INTEGER,
	city_id INTEGER,
	PRIMARY KEY (idstop),
	FOREIGN KEY(trip_id) REFERENCES `Trip` (idtrip),
	FOREIGN KEY(city_id) REFERENCES `City` (idcity)
);