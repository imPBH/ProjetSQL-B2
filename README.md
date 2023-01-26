# Projet SQL B2
This repo is the final project of a SQL course.

## Subject

The given subject was :

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

## Why did it have to be changed ?

The old database schema wasn't well structured.\
For example, the `tournament` table contains informations about the place where it is happening, but these informations aren't related to a tournament, they are related to a place, that's why we created a new `place` table in the new schema.

An other is example is the `staff`, `player` and `coach` table. They look pretty much the same, and all those people are employees. So we created a new table `employee_data` where we store all the common data instead of putting them in the `staff`, `player` and `coach` tables.
We kept those tables but now, they only contains a primary key for their ID, a foreign key for their employee ID, and specific data if needed, like `ranking` or `game` for players.

This is also safer, because we can't add someone into the `staff` table for example if they are not into the `employee_data` table.\
Another use of foreign keys that wasn't possible with the old schema, in the `tournament` table, we can only add a tournament with a place in the `place` table.


## How to run

You need to have sqlite3 installed.

In the same directory of the old database, in a terminal run this command to create an empty database\
```sqlite3 newdb.db "VACUUM;"```

Run this command to initialize the new database with the new schema\
```sqlite3 newdb.db < db_init.sql```

And then run this command to migrate data from the old database to the new one\
```sqlite3 tpb2.db < migrate.sql```

## Explanations
### Initialization script
In this sqlite script, we initialize the new database with the new schema.\
We create all the tables, all the columns and their type.

Here is an exemple of a simple table with a primary key\
![employee_data definition](https://user-images.githubusercontent.com/59230262/214820520-f8041c27-b12a-405d-8c39-d7272231de2f.png)

The first column is `IdEmployee`, this is the primary key of the table, we want it to be autoincremented so we dont have to specify the ID each time we add a new employee, and this column can't be null.\
For `Lastname`, `Firstname` and `Gender`, they are strings with a limit of 30 chars.\
The `Age` and `Wage` columns are integer numbers.

Here is an exemple of a table which uses a foreign key\
![staff definition](https://user-images.githubusercontent.com/59230262/214821632-301df8a4-0df9-4694-bf59-bd7fde4f7d49.png)

The first column is `Idstaff`, this is the primary key of the table, we want it to be autoincremented so we dont have to specify the ID each time we add a new staff, and this column can't be null.\
We define `IdEmployeeData` as an integer that can't be null because this will be our foreign key to the `employee_data` table.\
And then we say that `IdEmployeeData` is a foreign key, and it is a reference of `IdEmployee` in the `employee_data` table.

We can use multiple foreign keys in a table\
![tournament definition](https://user-images.githubusercontent.com/59230262/214822710-d283183e-926b-4a9f-9eec-a2d4f187d479.png)

### Migration script
In this sqlite script, we transfert data from the old database to the new one while respecting the new schema.

We start the script by indicating that we are starting a new transaction with the "BEGIN" command, we declare which tables we use and how we call them.\
![migration script start](https://user-images.githubusercontent.com/59230262/214943896-bc60491d-9c42-4d9b-9e47-fec22afb41d2.png)

Now we can start the migration. We should keep in mind that the order is very important here ! That's why we migrate data into tables that don't need foreign key.\
So we start by inserting data into the `employee_data` table.\
![insert staffs into employee_data](https://user-images.githubusercontent.com/59230262/214944599-2dd5ea35-2f7e-4412-b06c-a3bc92574403.png)

This one is pretty simple because all the data we need is available in the `staff` table in the old database. So we just retrieve all the data we need and insert them into our `employee_data` table in the new database.
We also do the same request for the `player` and `coach` tables in the old database because the `employee_data` need to contains all the data about all the employees, so we put everybody in this table.

Another table that doesn't use foreign keys is the `game` table. This one is actually the same as in the old database, it only contains an ID as a primary key and the name of the game. So we just need to retrieve the name into the old database and insert it into the new one, we don't need to retrieve the ID because it will be autoincremented.\
![insert into game](https://user-images.githubusercontent.com/59230262/214945881-8cfac6f8-1f3c-419a-bc25-2b50a1efce7e.png)

The `place` table is the last one that doesn't use foreign keys, but this one is a little bit more tricky because we need to retrieve the data about a place into the `tournament` table from the old database because the old one doesn't have a place table.\
We also use a `GROUP BY` clause because we want to be sure that we don't insert duplicate rows into our new table.\
![insert into place](https://user-images.githubusercontent.com/59230262/214946387-c45bd8e2-34e5-4d62-9777-88e92a5c3e4c.png)

Once that is done, we done all the simpliest part ! Now it's getting more tricky.\
We have to migrate data into table that use foreign keys, and so insert data from multiple tables into one new table.

A simple one is the new `staff` table.\
We only need to insert the `IdEmployee` from the new `employee_data` table into it. But we need to make sure the ID whe are inserting is part of the staff people ! So we need to compare the informations that we already had from the old `staff` table between the new `employee_data`table.\
To do that we will compare all the informations that we have about one person, so we make sure we are inserting the right person into the `staff` table.\
We can imagine that it is possible that there is more than one person with the same name and lastname, even if the odds are low, it is still possible, that's why we compare with all the data we have.\
![insert into staff](https://user-images.githubusercontent.com/59230262/214948371-8e82247f-0f26-4813-9f19-a5ea5fb6a1c8.png)

It will be the exact same process for the `player` and `coach` table as they look alike, the only difference is some columns, for example in the `player` table we need to retrieve the `IdGame` that was already into the old database, we kept the same order for the `game` table so we don't need to retrieve the ID into our new `game` table because the ID is already in the old `player` table.\

So for the last one, this one is a little bit different but the logic is the same.\
We need to insert the `IdPlace`, `IdGame`, `date` and `duration`. Our problem is that we can retrieve all this data from the old `tournament` table, except the `IdPlace` !\
That's why we also retrieve data from the new `place` table, and to make sure that we are inserting the right value, we compare every value we have about the place. In our case we compare the name of the place, the address and the city. This is necessary because it can be possible that 2 differents place have the same name, but not the same address for example.\
![insert into tournament](https://user-images.githubusercontent.com/59230262/214950459-90be168b-356a-4d54-942e-9dcd6b9d658b.png)

And at the end of the script, we close the transaction with the `COMMIT` command.
