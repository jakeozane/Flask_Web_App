SET FOREIGN_KEY_CHECKS=0;

#
#
#   INVENTORIES
#
#

DROP TABLE IF EXISTS `Inventories`;
CREATE TABLE `Inventories` (
	`inventoryID`		int(11) 			AUTO_INCREMENT,
	`location`	 		varchar(255) 		NOT	NULL,

CONSTRAINT PRIMARY KEY (inventoryID)

) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `Inventories` (`location`) VALUES
('San Miguel'),
('Orlando'),
('Portland, OR'),
('Debanville Falls'),
('Park City'),
('Phoenix'),
('Maine'),
('Austin'),
('Cape Cod'),
('Spokane, WA'),
('Coravllis'),
('Grand Rapids'),
('Arlington');

#
#
#   PRODUCTS
#
#

DROP TABLE IF EXISTS `Products`;
CREATE TABLE `Products` (
	`productID`			int(11) 		AUTO_INCREMENT,
	`productName` 		varchar(255) 	NOT	NULL,
	`description`		varchar(255),
	`price`				decimal(8,2)	NOT NULL,
	`inventoryID`		int(11)			DEFAULT NULL,

CONSTRAINT PRIMARY KEY (productID),
CONSTRAINT FOREIGN KEY (inventoryID) REFERENCES Inventories(inventoryID)

) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `Products` (`productName`, `description`, `price`, `inventoryID`) VALUES
('Bop-It', 'A toy that makes sounds and you have to react', 4.55, 1),
('Kazoo', 'A toy that turns your voice into a weird sound', 12.50, 3),
('Rubiks Cube', 'Puzzle Cube', 5.50, 3),
('Lego', 'A toy that makes weird sounds and you have to react', '4.99', 7),
('Cards Against Humanity', 'An offensive card game', '19.99', 13),
('Deck of Cards', '52 fancy pieces of paper', '5.98', 12),
('Lego', 'Toy bricks', '99.84', 8),
('Baker\'s Toy Set', 'Learn to bake with these plastic tools', '19.33', 6),
('Bop-It Premium', 'Super Premium Bop It', '9.99', 10),
('Bop It', 'Standard Edition Bop-It', '8.99', 10),
('Rubik\'s Cube', 'A puzzle cube', '19.99', 7),
('Rubik\'s Cube', 'Puzzle Cube with 6 Sides', '18.94', 12);

#
#
#   SALE DATA
#
#

DROP TABLE IF EXISTS `SaleData`;
CREATE TABLE `SaleData` (
	`purchaseID`		int(11) 		AUTO_INCREMENT,
	`userID`	 		int(11)		 	NOT	NULL,
	`total`				decimal(8,2)	NOT NULL,

CONSTRAINT PRIMARY KEY (purchaseID),
CONSTRAINT FOREIGN KEY (userID) REFERENCES UserData(userID)

) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `SaleData` (`userID`, `total`) VALUES
(1, 5.50),
(2, 12.50),
(1, 55.10),
(3, 5.70),
(1, 5.50),
(2, 12.50),
(1, 55.10),
(3, 5.70),
(3, 3.33),
(3, 12.44),
(7, 444.53),
(3, 25.55),
(9, 199.28),
(8, 192.40),
(7, 889.30),
(5, 32.80),
(7, 2.39);

#
#
#   PRODUCTS PURCHASED
#
#

DROP TABLE IF EXISTS `ProductsPurchased`;
CREATE TABLE `ProductsPurchased` (
	`productID`			int(11),
	`purchaseID`		int(11),

CONSTRAINT FOREIGN KEY (productID) REFERENCES Products(productID),
CONSTRAINT FOREIGN KEY (purchaseID) REFERENCES SaleData(purchaseID)

) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `ProductsPurchased` (`productID`, `purchaseID`) VALUES
(1, 1),
(1, 2),
(2, 1),
(2, 2),
(2, 3),
(3, 2),
(7, 1),
(9, 1),
(9, 2),
(9, 5),
(10, 3),
(10, 5),
(9, 2),
(7, 2),
(4, 4),
(8, 3),
(10, 8),
(6, 10),
(4, 11),
(2, 9),
(4, 12);

#
#
#   USER DATA
#
#

DROP TABLE IF EXISTS `UserData`;
CREATE TABLE `UserData` (
	`userID`			int(11) 		AUTO_INCREMENT,
	`firstName`	 		varchar(255) 	NOT	NULL,
	`lastName`	 		varchar(255) 	NOT	NULL,
	`streetAddress`		varchar(255) 	NOT	NULL,
	`zipCode`			int(11)			NOT NULL,
	`countryCode`		int(11)			NOT NULL,
	`thirdPartyID`		int(11)			NOT NULL,

CONSTRAINT PRIMARY KEY (userID),
CONSTRAINT FOREIGN KEY (thirdPartyID) REFERENCES ThirdParties(thirdPartyID)

) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `UserData` (`firstName`, `lastName`, `streetAddress`, `zipCode`, `countryCode`, `thirdPartyID`) VALUES
('James', 'Apples', '123 Main Street', 98844, 1, 1),
('Dominic', 'Green', '122 South Baker Street', 22445, 1, 2),
('John', 'Doe', '333 Main Street', 98844, 1, 1),
('Jane', 'Doe', 'Park Ave Apartments, 3301 South Kane Street', 98904, 1, 3),
('Gene', 'Tens', '10992 SW Canary Lane, APT 02B', 91002, 12, 2),
('Deans', 'Thomas', '123 Main St.', 98991, 0, 7),
('Blake', 'Rogers', '19922 SW Beach Street, APT 199B', 92111, 2, 8),
('Don', 'Thomas', '10 Main ST', 28394, 9, 5),
('Gordon', 'Ramsay', '16 Undercooked Bass Rd.', 1928, 19, 9);

#
#
#   THIRD PARTIES
#
#

DROP TABLE IF EXISTS `ThirdParties`;
CREATE TABLE `ThirdParties` (
	`thirdPartyID`		int(11) 		AUTO_INCREMENT,
	`thirdPartyName`	varchar(255) 	NOT	NULL,
	`description`		varchar(255),

CONSTRAINT PRIMARY KEY (thirdPartyID)

) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `ThirdParties` (`thirdPartyName`, `description`) VALUES
('NSA', 'Not the national Security Agency, definitely not.'),
('Dow Logical', 'Retailer of Questionable User Data'),
('Facebook', 'This one is too easy'),
('Google', '...would never collect user data without your consent... right'),
('Interpol', 'International Police'),
('US DOJ', 'United States Department of Justice'),
('ThirdPartyContractors (tm)', 'Definitely not NSA operating out of small businesses'),
('NSA-SSD', 'Super Spying Division of the NSA'),
('CIA', 'Central Intelligence Agency');

SET FOREIGN_KEY_CHECKS=1;