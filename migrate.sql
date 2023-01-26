BEGIN;

ATTACH DATABASE 'tpb2.db' AS old;
ATTACH DATABASE 'newdb.db' AS new;

INSERT INTO new.employee_data (Lastname, Firstname, Gender, Age, Wage) 
SELECT 
  lastname, 
  firstname, 
  gender, 
  age, 
  wage 
FROM 
  old.staff;

INSERT INTO new.employee_data (Lastname, Firstname, Gender, Age, Wage) 
SELECT 
  lastname, 
  firstname, 
  gender, 
  age, 
  wage 
FROM 
  old.player;

INSERT INTO new.employee_data (Lastname, Firstname, Gender, Age, Wage) 
SELECT 
  lastname, 
  firstname, 
  gender, 
  age, 
  wage 
FROM 
  old.coach;

INSERT INTO new.game (Name) 
SELECT 
  name 
FROM 
  old.game;

INSERT INTO new.place (Name, Address, City) 
SELECT 
  placeName, 
  address, 
  city 
FROM 
  old.tournament 
GROUP BY 
  placeName, 
  address, 
  city;

INSERT INTO new.staff (IdEmployeeData) 
SELECT 
  IdEmployee 
FROM 
  new.employee_data, 
  old.staff 
WHERE 
  new.employee_data.Lastname = old.staff.lastname 
  AND new.employee_data.Firstname = old.staff.firstname
  AND new.employee_data.Gender = old.staff.gender
  AND new.employee_data.Age = old.staff.age
  AND new.employee_data.Wage = old.staff.wage;

INSERT INTO new.player (IdGame, Ranking, IdEmployeeData) 
SELECT 
  IdGame, 
  ranking, 
  IdEmployee 
FROM 
  old.player, 
  new.employee_data 
WHERE 
  new.employee_data.Lastname = old.player.lastname 
  AND new.employee_data.Firstname = old.player.firstname
  AND new.employee_data.Gender = old.player.gender
  AND new.employee_data.Age = old.player.age
  AND new.employee_data.Wage = old.player.wage;

INSERT INTO new.coach (IdGame, LicenseDate, IdEmployeeData) 
SELECT 
  IdGame, 
  licenseDate, 
  IdEmployee 
FROM 
  old.coach, 
  new.employee_data 
WHERE 
  new.employee_data.Lastname = old.coach.lastname 
  AND new.employee_data.Firstname = old.coach.firstname
  AND new.employee_data.Gender = old.coach.gender
  AND new.employee_data.Age = old.coach.age
  AND new.employee_data.Wage = old.coach.wage;

INSERT INTO new.tournament (IdPlace, IdGame, Date, Duration) 
SELECT 
  IdPlace, 
  IdGame, 
  date, 
  duration 
FROM 
  old.tournament, 
  new.place 
WHERE 
  old.tournament.placeName = new.place.Name
  AND old.tournament.address = new.place.Address
  AND old.tournament.city = new.place.City;

COMMIT;
