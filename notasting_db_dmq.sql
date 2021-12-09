-- ":" used to denote variables that will be input by the user

-- ******************** CRUD ***************************

-- C(reate):
/********************************************************
Inventory
********************************************************/
-- Query to add a new inventory
INSERT INTO Inventories (inventoryID, location) VALUES (:inventoryID, :location);

/********************************************************
Products
********************************************************/
-- Query to add a new product
INSERT INTO Products (productID, productName, description, price, inventoryID) VALUES (:productID, :productName, :description, :price, :inventoryID);

/********************************************************
Products Purchased
********************************************************/
-- Query to add a new purchased product
INSERT INTO ProductsPurchased (productID, purchaseID) VALUES (:productID, :purchaseID);

/********************************************************
Sales Data
********************************************************/
-- Query to add new sales data
INSERT INTO SalesData (purchaseID, userID, total) VALUES (:purchaseID, :userID, :total);

/********************************************************
User Data
********************************************************/
-- Query to add new user data
INSERT INTO UserData (userID, firstName, lastName, streetAddress, zipCode, countryCode, thirdPartyID) VALUES (:userID, :firstName, :lastName, :streetAddress, :zipCode, :countryCode, :thirdPartyID);

/********************************************************
Third Partties
********************************************************/
-- Query to add new third party
INSERT INTO ThirdParties (thirdPartyID, thirdPartyName, description) VALUES (:thirdPartyID, :thirdPartyName, :description);

-- R(ead):
/********************************************************
Inventory
********************************************************/
-- Query to read from Inventories
SELECT * FROM Inventories;

-- Query to search in Inventories sorted by location descending
SELECT * FROM Inventories WHERE (inventoryID like '%:input%' OR location like '%:input%')
ORDER BY location DESC;

/********************************************************
Products
********************************************************/
-- Query to read from Products
SELECT * FROM Products;

-- Query to search in Products sorted by productName descending
SELECT * FROM Products WHERE (productID like '%:input%' OR productName like '%:input%' OR description like '%:input%' OR price like '%:input%' OR inventoryID like '%:input%')
ORDER BY productName DESC;

/********************************************************
Products Purchased
********************************************************/
-- Query to read from ProductsPurchased
SELECT * FROM ProductsPurchased;

-- Query to search in ProductsPurchased
SELECT * FROM ProductsPurchased WHERE (productID like '%:input%' OR purchaseID like '%:input%');

/********************************************************
Sales Data
********************************************************/
-- Query to read from SalesData
SELECT * FROM SalesData;

-- Query to search in SalesData
SELECT * FROM SalesData WHERE (purchaseID like '%:input%' OR userID like '%:input%' OR total like '%:input%');

/********************************************************
User Data
********************************************************/
-- Query to read from UserData
SELECT * FROM UserData;

-- Query to search in Products sorted by firstName descending
SELECT * FROM UserData WHERE (userID like '%:input%' OR firstName like '%:input%' OR lastName like '%:input%' OR streetAddress like '%:input%' OR zipCode like '%:input%' OR countryCode like '%:input%' OR thirdPartyID like '%:input%')
ORDER BY firstName DESC;

/********************************************************
Third Partties
********************************************************/
-- Query to read from ThirdParties
SELECT * FROM ThirdParties;

-- Query to search in Inventories sorted by thirdPartyName descending
SELECT * FROM ThirdParties WHERE (thirdPartyID like '%:input%' OR thirdPartyName like '%:input%' OR description like '%:input%')
ORDER BY thirdPartyName DESC;

-- U(pdate)
/********************************************************
Update Inventory
********************************************************/
-- Query to update an inventory in Inventories based on a provided inventoryID
UPDATE Inventories SET location = (:location_input) WHERE inventoryID = (:inventoryID)

/********************************************************
Update Products
********************************************************/
-- Query to update a product in Products based on a provided productID
UPDATE Products SET productName = (:productName_input), description = (:description_input), price = (:price_input) WHERE productID = (:productID)

/********************************************************
Update Products Purchased
********************************************************/
-- Query to update a purchased product in ProductsPurchased based on a provided productID
UPDATE ProductsPurchased SET purchaseID = (:purchaseID_input) WHERE productID = (:productID)

/********************************************************
Update Sales Data
********************************************************/
-- Query to update a sale in SalesData based on a provided purchaseID
UPDATE SalesData SET userID = (:userID_input), total = (:total_input) WHERE purchaseID = (:purchaseID)

/********************************************************
Update User Data
********************************************************/
-- Query to update a user in UserData based on a provided userID
UPDATE UserData SET firstName = (:firstName_input), lastName = (:lastName_input), streetAddress = (:streetAddress_input), zipCode = (:zipCode_input), countryCode = (:countryCode_input), thirdPartyID = (:thirdPartyID_input) WHERE userID = (:userID)

/********************************************************
Update Third Parties
********************************************************/
-- Query to update a third party in ThirdParties based on a provided thirdPartyIDID
UPDATE ThirdParties SET thirdPartyName = (:thirdPartyName_input), description = (:description_input) WHERE thirdPartyID = (:thirdPartyID)

-- D(elete):
/********************************************************
Inventory
********************************************************/
-- Query to delete an inventory from Inventories based on a provided inventoryID
DELETE FROM Inventories WHERE inventoryID = (:inventoryID);

/********************************************************
Products
********************************************************/
-- Query to delete a product from Products based on a provided productID
DELETE FROM Products WHERE productID = (:productID);

/********************************************************
Products Purchased
********************************************************/
-- Query to delete a M:M purchased product from ProductsPurchased based on a provided productID and purchaseID
DELETE FROM ProductsPurchased WHERE (productID = (:productID) AND purchaseID = (:purchaseID));

/********************************************************
Sales Data
********************************************************/
-- Query to delete a sale from SalesData based on a provided purchaseID
DELETE FROM SalesData WHERE purchaseID = (:purchaseID);

/********************************************************
User Data
********************************************************/
-- Query to delete a user from UserData based on a provided userID
DELETE FROM UserData WHERE userID = (:userID);

/********************************************************
Third Parties
********************************************************/
-- Query to delete a third party from ThirdParties based on a provided thirdPartyID
DELETE FROM ThirdParties WHERE thirdPartyID = (:thirdPartyID);
