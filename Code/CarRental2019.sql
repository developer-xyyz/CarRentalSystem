CREATE DATABASE CarRentalDatabase;
USE CarRentalDatabase;

CREATE TABLE CUSTOMER ( 
CustID INT NOT NULL PRIMARY KEY AUTO_INCREMENT , 
Name VARCHAR(100) ,
 Phone VARCHAR(100)
);

CREATE TABLE RATE ( 
Type INT NOT NULL , 
Category INT NOT NULL , 
Weekly INT  NOT NULL , 
Daily INT NOT NULL, 
CONSTRAINT VehicleType PRIMARY KEY(Type , Category)
);

CREATE TABLE VEHICLE (
VehicleID VARCHAR(30) NOT NULL PRIMARY KEY , 
Description VARCHAR(100) NOT NULL , 
Year  INT NOT NULL , 
Type INT NOT NULL , 
Category INT NOT NULL , 
FOREIGN KEY (Type , Category) REFERENCES RATE(Type , Category)  
ON DELETE NO ACTION ON UPDATE CASCADE
);

CREATE TABLE RENTAL ( 
CustID INT NOT NULL , 
VehicleID VARCHAR(30) NOT NULL , 
StartDate VARCHAR(30) , 
OrderDate VARCHAR(30) , 
RentalType INT , 
Qty INT ,
 ReturnDate VARCHAR(30) , 
TotalAmount INT  , 
PaymentDate VARCHAR(30) , 
FOREIGN KEY (CustID) REFERENCES CUSTOMER(CustID) ON DELETE NO ACTION ON UPDATE CASCADE , FOREIGN KEY (VehicleID) REFERENCES VEHICLE(VehicleID) ON DELETE NO ACTION ON UPDATE CASCADE
);

SET SQL_SAFE_UPDATES = 0;

-- part 2 queries

-- query 1
INSERT INTO CUSTOMER(Name , Phone) VALUES ('Ishan Poudel' , '(405)981-8094');
INSERT INTO CUSTOMER(Name , Phone) VALUES ('Ahnaf Ahmad','(817)123-4567');

-- query 2
UPDATE CUSTOMER SET PHONE = '(817)721-8965' WHERE NAME = 'Ishan Poudel';
UPDATE CUSTOMER SET PHONE = '(817)721-8965' WHERE NAME = 'Ahnaf Ahmad';

-- query 3
UPDATE RATE SET Daily= Daily * 1.05 WHERE CATEGORY = '1';

-- query 4 a 
INSERT INTO VEHICLE (VehicleID , Description , Year , Type , Category) VALUES
 ('5FNRL6H58KB133711 ' , 'Honda Odyssey' , '2019' , '6' , '1' );

-- query 4 b RUN THIS BEFORE 4 a

INSERT INTO RATE (Type , Category , Weekly , Daily) VALUES ('5' , '1' , '900' , '150');
INSERT INTO RATE (Type , Category , Weekly , Daily) VALUES ('6' , '1' , '800' , '135');

-- query 5
SELECT R.VehicleID as VIN , VH.Description , VH.Year , SUM(R.Qty*R.RentalType) 
AS Total FROM
(SELECT * FROM VEHICLE WHERE TYPE='1' and Category='1') As VH , 
RENTAL AS R 
WHERE VH.VehicleID=R.VehicleID AND 
R.VehicleID NOT IN 
(SELECT RENTAL.VehicleID FROM RENTAL 
WHERE (StartDate>='2019-06-01' AND StartDate <= '2019-06-20') OR 
(ReturnDate <= '2019-06-20' AND ReturnDate>='2019-06-01'))
 GROUP BY VH.VehicleID;

-- query 6
SELECT name , SUM(TotalAmount) 
FROM customer as c , 
rental as r WHERE C.CustID = R.CustID AND C.CustID = '221' 
AND R.PaymentDate IS NULL;

-- query 7
SELECT V.VehicleID as VIN, V.Description, V.Year, 
CASE
	WHEN V.Category = 1 THEN 'Luxury'
   	WHEN V.Category = 0 THEN 'Basic'
END as Category,
CASE
	WHEN V.Type = 1 THEN 'Compact'
    	WHEN V.Type = 2 THEN 'Medium'
    	WHEN V.Type = 3 THEN 'Large'
    	WHEN V.Type = 4 THEN 'SUV'
    	WHEN V.Type = 5 THEN 'Truck'
    	WHEN V.Type = 6 THEN 'Van'
END as Type, R.Daily, R.Weekly
FROM VEHICLE as V, Rate as R
WHERE (V.Type = R.Type AND V.Category = R.Category)
ORDER BY V.Category desc, V.Type asc;

-- query 8
SELECT SUM(TotalAmount) as 
TotalAmount FROM RENTAL AS R 
WHERE R.PaymentDate IS NOT NULL;


-- query 9
SELECT V.Description, V.Year, 
CASE
	WHEN V.Category = 1 THEN 'Luxury'
   	 WHEN V.Category = 0 THEN 'Basic'
END as Category,
CASE
	WHEN V.Type = 1 THEN 'Compact'
    	WHEN V.Type = 2 THEN 'Medium'
    	WHEN V.Type = 3 THEN 'Large'
   	WHEN V.Type = 4 THEN 'SUV'
    	WHEN V.Type = 5 THEN 'Truck'
   	WHEN V.Type = 6 THEN 'Van'
END as Type,
R.TotalAmount as UnitPrice, 
CASE
	WHEN R.PaymentDate is NULL THEN 'False'
    	ELSE 'True'
END as Paid,
CASE
	WHEN R.RentalType = 1 THEN 'Daily'
    	WHEN R.RentalType = 7 THEN 'Weekly'
END as RentalType,
R.Qty as Duration
FROM VEHICLE as V, RENTAL as R, CUSTOMER as C
WHERE R.CustID = C.CustID AND R.VehicleID = V.VehicleID AND C.Name = 'J. Brown'
ORDER by R.StartDate asc;

-- query 9b 

SELECT SUM( R.TotalAmount) as CurrentBalance
FROM RENTAL as R, CUSTOMER as C
WHERE (C.Name = 'J. Brown' AND R.CustID = C.CustID AND R.PaymentDate IS NULL);

-- query 10
SELECT C.Name, R.StartDate, R.ReturnDate, R.TotalAmount
FROM RENTAL AS R, CUSTOMER AS C
WHERE R.CustID = C.CustID AND R.VehicleID = '19VDE1F3XEE414842' AND R.PaymentDate IS
NULL;

-- query 11
SELECT * from CUSTOMER WHERE CustID NOT IN (SELECT CustID FROM RENTAL);

-- query 12
SELECT C.Name, V.Description, R.StartDate, R.ReturnDate, R.TotalAmount, R.PaymentDate
FROM CUSTOMER as C, VEHICLE as V, RENTAL as R
WHERE C.CustID = R.CustID AND V.VehicleID = R.VehicleID AND R.StartDate = R.PaymentDate
ORDER by C.Name asc;


-- part 3, task 1 queries
 
-- query 1
ALTER TABLE RENTAL ADD Returned INT;
UPDATE RENTAL SET Returned = 1 WHERE PaymentDate IS NOT NULL;
UPDATE RENTAL SET Returned = 0 WHERE PaymentDate IS  NULL;

-- query 2
CREATE VIEW vRentalInfo AS
select 
r.OrderDate , 
r.StartDate , 
r.ReturnDate , 
DATEDIFF(r.ReturnDate , r.OrderDate) AS 'TotalDays',  
v.VehicleID AS 'VIN' , 
v.Description  AS 'VEHICLE', 

CASE 
WHEN v.Type=1 THEN 'COMPACT'
WHEN v.Type=2 THEN 'Medium'
WHEN v.Type=3 THEN 'Large'
WHEN v.Type=4 THEN 'SUV'
WHEN v.Type=5 THEN 'Truck'
WHEN v.Type=6 THEN 'Van'
END AS 'Type' ,

CASE
WHEN v.Category = 0 THEN 'BASIC'
WHEN v.Category = 1 THEN 'LUXURY'
END AS 'Category',

 r.CustID AS 'CustomerID',

c.Name AS 'CustomerName', 
r.TotalAmount as 'OrderAmount' ,

CASE 
WHEN r.PaymentDate is NULL THEN TotalAmount
ELSE 0
END AS 'RentalBalance'

FROM rental r 

JOIN vehicle v on r.VehicleID = v.VehicleID 
JOIN customer c on c.custID = r.CustID 
ORDER BY r.StartDate ASC;





