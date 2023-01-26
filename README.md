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
