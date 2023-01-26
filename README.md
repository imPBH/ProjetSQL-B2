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

