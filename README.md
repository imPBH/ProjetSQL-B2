# Projet SQL B2
This repo is the final project of a SQL course.

## Summary

- [Subject](#subject)
- [Why did it have to be changed ?](#why-did-it-have-to-be-changed)
- [How to run](#how-to-run)
    - [Migration](#migration)
    - [Python script](#python-script)
- [Explanations](#explanations)
    - [Initialization script](#initialization-script)
    - [Migration script](#migration-script)
    - [Python script](#python-script-1)
        - [List every tournament for a given game name](#list-every-tournament-for-a-given-game-name)
        - [Given a game name, retrieve the average wage of the players](#given-a-game-name-retrieve-the-average-wage-of-the-players)
        - [List all tournaments by place](#list-all-tournaments-by-place)
        - [Get the number of players by gender](#get-the-number-of-players-by-gender)
    
## Subject

The given subject was:


You’ve been contacted by TeamLikwid to migrate their old database to their new schema.
They want you to:
- Create a .sql script that’ll create the new database schema
- Create a second script that’ll transfer data from the old DB to the new one

In addition, to make sure they still can access their data, they want you to show the queries + results for the followings:
- List every tournament for a given game name
- Given a game name, retrieve the average wage of the players
- List all tournament by place
- Get the number of players by gender

Here is the old database schema:

![Old schema](https://user-images.githubusercontent.com/59230262/214812074-a0aca6a2-bc23-45f8-848d-3e6de00c8b48.png)

Here is the new schema

![New schema](https://user-images.githubusercontent.com/59230262/214812633-c1254f12-c400-4ba9-b3b0-30038e7dcca8.png)

## Why did it have to be changed

The old database schema wasn't well structured.\
For example, the `tournament` table contains information about the place where it is happening, but this information isn't related to a tournament, it relates to a place, that's why we created a new `place` table in the new schema.

Another example is the `staff`, `player` and `coach` table. They look pretty much the same, and all those people are employees. So we created a new table `employee_data` where we store all the common data instead of putting them in the `staff`, `player` and `coach` tables.
We kept those tables, but now, they only contain a primary key for their ID, a foreign key for their employee ID, and specific data if needed, like `ranking` or `game` for players.

This is also safer, because we can't add anyone into the `staff` table for if they are not in the `employee_data` table because of the use of foreign keys.\
Another use of foreign keys which was not possible with the old schema, in the new `tournament` table we can only add a tournament with a place which is in the `place` table because we are using the `place` primary key as a foreign key in the `tournament` table. So inserting a new tournament with an `IdPlace` that does not exist will result in an error and the tournament will not be inserted because it does not meet the foreign key constraint

## How to run

###  Migration
You need to have [sqlite3](https://www.sqlite.org/download.html) installed.

In the same directory of the old database, in a terminal run this command to create an empty database\
```sqlite3 newdb.db "VACUUM;"```

Run this command to initialize the new database with the new schema\
```sqlite3 newdb.db < db_init.sql```

And then run this command to migrate data from the old database to the new one\
```sqlite3 tpb2.db < migrate.sql```

### Python script
You need to have [Python](https://www.python.org/downloads/) installed.

Run this command to launch the script\
```python main.py```\
or\
```python3 main.py```


## Explanations
### Initialization script
In this sqlite script, we initialize the new database with the new schema.\
We create all the tables, all the columns and their type.

Here is an example of a simple table with a primary key
```SQL
CREATE TABLE IF NOT EXISTS "employee_data"
(
    IdEmployee INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    Lastname VARCHAR2(30),
    Firstname VARCHAR2(30),
    Gender VARCHAR2(30),
    Age INT,
    Wage INT
);
```

The first column is `IdEmployee`, this is the primary key of the table, we want it to be autoincremented so we dont have to specify the ID each time we add a new employee, and this column can't be null.\
For `Lastname`, `Firstname` and `Gender`, they are strings with a limit of 30 chars.\
The `Age` and `Wage` columns are integer numbers.

Here is an example of a table which uses a foreign key
```SQL
CREATE TABLE IF NOT EXISTS "staff"
(
    IdStaff INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    IdEmployeeData INTEGER NOT NULL,
    FOREIGN KEY(IdEmployeeData) REFERENCES employee_data(IdEmployee)
);
```

The first column is `Idstaff`, this is the primary key of the table, we want it to be autoincremented so we don't have to specify the ID each time we add a new staff, and this column can't be null.\
We define `IdEmployeeData` as an integer that can't be null because this will be our foreign key to the `employee_data` table.\
And then we say that `IdEmployeeData` is a foreign key, and it is a reference of `IdEmployee` in the `employee_data` table.

We can use multiple foreign keys in a table
```SQL
CREATE TABLE IF NOT EXISTS "tournament"
(
    IdTournament INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    IdPlace INTEGER NOT NULL,
    IdGame INTEGER NOT NULL,
    Date VARCHAR2(30) NOT NULL,
    Duration INTEGER,
    FOREIGN KEY(IdPlace) REFERENCES place(IdPlace),
    FOREIGN KEY(IdGame) REFERENCES game(IdGame)
);
```

### Migration script
In this sqlite script, we transfer data from the old database to the new one while respecting the new schema.

We start the script indicating that we are starting a new transaction with the `BEGIN` command, we declare which tables we use and how we call them.
```SQL
BEGIN;

ATTACH DATABASE 'tpb2.db' AS old;
ATTACH DATABASE 'newdb.db' AS new;
```

Now we can start the migration. We should keep in mind that the order is very important here! That's why we migrate data into tables that don't need foreign key.\
So we start by inserting data into the `employee_data` table.
```SQL
INSERT INTO new.employee_data (Lastname, Firstname, Gender, Age, Wage) 
SELECT 
  lastname, 
  firstname, 
  gender, 
  age, 
  wage 
FROM 
  old.staff;
 ```
 
This one is pretty simple because all the data we need is available in the `staff` table in the old database. So we just retrieve all the data we need and insert them into our `employee_data` table in the new database.
We also make the same request for the `player` and `coach` tables in the old database because the `employee_data` need to contain all the data about all the employees, so we put everybody in this table.

Another table that doesn't use foreign keys is the `game` table. This one is actually the same as in the old database, it only contains an ID as a primary key and the name of the game. So, we just need to retrieve the name into the old database and insert it into the new one, we don't need to retrieve the ID because it will be autoincremented.
```SQL
INSERT INTO new.game (Name) 
SELECT 
  name 
FROM 
  old.game;
```

The `place` table is the last one that doesn't use foreign keys, but this one is a little bit more tricky because we need to retrieve the data about a place into the `tournament` table from the old database because the old one doesn't have a place table.\
We also use a `GROUP BY` clause because we want to be sure that we don't insert duplicate rows into our new table.
```SQL
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
```

Once that is done, we have done all the simplest part! Now it's getting more tricky.\
We have to migrate data into a table that uses foreign keys, and so insert data from multiple tables into one new table.

A simple one is on the new `staff` table.\
We only need to insert the `IdEmployee` from the new `employee_data` table into it. But we need to make sure the ID we are inserting is part of the staff people ! So we need to compare the information that we already had from the old `staff` table between the new `employee_data`table.\
To do that we will compare all the information that we have about one person, so we make sure we are inserting the right person into the `staff` table.\
We can imagine that it is possible that there is more than one person with the same name and last name, even if the odds are low, it is still possible, that's why we compare with all the data we have.
```SQL
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
```

It will be the exact same process for the `player` and `coach` table as they look alike, the only difference is between some columns. For example in the `player` table, we need to retrieve the `IdGame` that was already in the old database, we kept the same order for the `game` table so we don't need to retrieve the ID into our new `game` table because the ID is already in the old `player` table.

So for the last one, this one is a little bit different but the logic is the same.\
We need to insert the `IdPlace`, `IdGame`, `date` and `duration`. Our problem is that we can retrieve all this data from the old `tournament` table, except the `IdPlace`!\
That's why we also retrieve data from the new `place` table, and to make sure that we are inserting the right value, we compare every value we have about the place. In our case, we compare the name of the place, the address and the city. This is necessary because it can be possible that 2 different places have the same name, but not the same address for example.
```SQL
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
```

And at the end of the script, we close the transaction with the `COMMIT` command.

### Python script

This Python script uses the `sqlite3` library.\
We use it to demonstrate that the new database is fully functional.

In the `main` function, we just create a connection to our database and create a context by creating a cursor on the database. This context will be provided to functions that need to execute a request in the database.
```python
def main():
    connection = sqlite3.connect("newdb.db")
    context = connection.cursor()
```
#### List every tournament for a given game name
To list every tournament for a given game name, we run the `print_all_tournaments_for_game` function.
This function will call the `choose_game` function which will call the `get_games` function.\
The `get_games` will return the list of all games in the database, the request used is
```SQL
SELECT
  Name 
FROM
  game
```

Once the user has chosen a game, we will execute this request
```python
query = """
    SELECT 
      Date, 
      place.Name, 
      place.Address, 
      place.City, 
      Duration 
    FROM 
      tournament 
      INNER JOIN game on game.IdGame = tournament.IdGame 
      INNER JOIN place on place.IdPlace = tournament.IdPlace 
    WHERE 
      game.Name = :game_name"""

par = {"game_name": game_name}
res = context.execute(query, par)
```

Here is the outputs for each game one by one\
![list smash tournaments](https://user-images.githubusercontent.com/59230262/214962157-1d67eba8-1490-4f3a-a605-ead1bf15279a.png)\
![list tekken tournaments](https://user-images.githubusercontent.com/59230262/214962338-05f552ec-3833-4dc5-af72-db5c1028f072.png)\
![list streetfighter tournaments](https://user-images.githubusercontent.com/59230262/214962403-115ed799-0a5c-4f9a-9ae4-5f7b1170ec75.png)\
![list lol tournaments](https://user-images.githubusercontent.com/59230262/214962478-fc082bdd-d801-4a79-8563-64078baabe82.png)\
![list csgo tournaments](https://user-images.githubusercontent.com/59230262/214962561-a1ab119b-908b-4cd5-83a9-c073a8b3f008.png)\
![list apex tournaments](https://user-images.githubusercontent.com/59230262/214962615-08c36f6b-8dfe-48e8-9f41-4c3723e78fdb.png)

#### Given a game name, retrieve the average wage of the players
To retrieve the average wage of the players by a given game name, we run the `print_average_wage_for_game` function.\
This function will call the `choose_game` function like the `print_all_tournaments_for_game`.\
The request used is
```python
query = """
    SELECT 
      AVG(Wage) 
    FROM 
      player 
      INNER JOIN employee_data ON employee_data.IdEmployee = player.IdEmployeeData 
      INNER JOIN game ON game.IdGame = player.IdGame 
    WHERE 
      game.Name = :game_name"""

par = {"game_name": game_name}
res = context.execute(query, par)
```

Here is the outputs for each game one by one\
![average wage smash](https://user-images.githubusercontent.com/59230262/214963668-87c2b8d3-bd15-401c-b209-a36173266422.png)\
![average wage tekken](https://user-images.githubusercontent.com/59230262/214963713-1c27548f-bacc-493f-ac12-c98553b93049.png)\
![average wage streetfighter](https://user-images.githubusercontent.com/59230262/214963859-0b3ef53f-5e30-47a0-b2f6-89beefe7c667.png)\
![average wage lol](https://user-images.githubusercontent.com/59230262/214963785-72943971-5945-4665-82ff-05d214180c30.png)\
![average wage csgo](https://user-images.githubusercontent.com/59230262/214963935-02b729a2-7c06-4b02-93c9-c0fcb30b8a00.png)\
![average wage apex](https://user-images.githubusercontent.com/59230262/214963983-43a64b62-4a31-4d74-9f03-ac1223aa7cc8.png)

#### List all tournaments by place
To list all tournaments by place, we run the `print_tournaments_by_places` function.\
This function will call the `get_places` function that will return the list of all places in the database.\
The request used to retrieve places is
```SQL
SELECT 
  * 
FROM 
  place
```

Once we have all places, we will loop on them and run the `get_tournaments_by_place` that will return the list of tournaments given a place.\
The request used for this is
```python
query = """
    SELECT 
      * 
    FROM 
      tournament 
    WHERE 
      IdPlace = :idPlace"""

par = {"idPlace": place[0]}
res = context.execute(query, par)
```

Here is the output\
![list all tournaments by place output](https://user-images.githubusercontent.com/59230262/214965158-76802479-36a0-4ca9-b9e0-dfc5308e81af.png)

We also could have used this request to do this in only one request
```SQL
SELECT
  game.Name,
  tournament.Date,
  tournament.Duration,
  place.Name,
  place.Address,
  place.City
FROM
  tournament
INNER JOIN game ON game.IdGame = tournament.IdGame
INNER JOIN place on place.IdPlace = tournament.IdPlace
ORDER BY place.IdPlace
```

Here is the output\
![list all tournaments by place alt output](https://user-images.githubusercontent.com/59230262/214966348-ca4c7615-11c7-461f-a6f8-0eff899ec3c9.png)\
We didn't use this one because it was not possible to print the output like we did with the loop on tournaments.

#### Get the number of players by gender
To get the number of players by gender, we run the `print_number_of_players_by_gender` function.\
The request used for this is
```python
query = """
    SELECT 
      gender, 
      COUNT(gender) 
    FROM 
      player 
      INNER JOIN employee_data ON employee_data.IdEmployee = player.IdEmployeeData 
    GROUP BY 
      Gender"""

res = context.execute(query)
genders = res.fetchall()
```

Here is the output\
![number of players by gender](https://user-images.githubusercontent.com/59230262/214967822-4f53dcce-447d-485f-a08e-d52bf5ed6df6.png)
