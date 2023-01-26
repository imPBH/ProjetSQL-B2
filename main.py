import sqlite3


def get_games(context):
    '''Return all games in the DB'''

    query = """
    SELECT 
      Name 
    FROM 
      game"""

    res = context.execute(query)
    games = []
    for result in res:
        games.append(result[0])
    return games

 
def get_game_by_id(context, id):
    '''Return the name of a game by a given id'''

    query = """
    SELECT 
      Name 
    FROM 
      game 
    WHERE 
      IdGame = :id"""

    par = {"id": id}
    res = context.execute(query, par)
    game = res.fetchone()[0]
    return game


def get_places(context):
    '''Return all places in the DB'''

    query = """
    SELECT 
      * 
    FROM 
      place"""

    res = context.execute(query)
    places = res.fetchall()
    return places


def get_tournaments_by_place(context, place):
    '''Return all tournaments by a given place'''

    query = """
    SELECT 
      * 
    FROM 
      tournament 
    WHERE 
      IdPlace = :idPlace"""

    par = {"idPlace": place[0]}
    res = context.execute(query, par)
    tournaments = res.fetchall()
    return tournaments


def choose_game(context):
    '''Return the ID of a game choosen by the user'''

    games = get_games(context)
    try:
        print("Choose a game:\n")
        for index, game in enumerate(games):
            print(f"{index}. {game}")
        choice = int(input("\nYour choice: "))
    except ValueError:
        # If user doesn't enter a number, prints an error message and returns none
        print("Please enter a valid number\n")
        return None

    try:
        return games[choice]
    except IndexError:
        # If user doesn't enter a valid number, prints an error message and returns none
        print("Please enter a valid number\n")
        return None


def print_all_tournaments_for_game(context):
    '''Print every tournament for a given game name'''

    # Have the user choose a game 
    game = None
    while game == None:
        game = choose_game(context)

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
      game.Name = :game"""

    par = {"game": game}
    res = context.execute(query, par)
    tournaments = res.fetchall()

    if len(tournaments) == 0:
        print(f"There is no tournaments for {game}")
        return

    print(f"\nAll tournaments for {game} :")
    for tournament in tournaments:
        print(
            f"Date: {tournament[0]} | Place: {tournament[1]}, {tournament[2]}, {tournament[3]} | Duration: {tournament[4]}"
        )


def print_average_wage_for_game(context):
    '''Given a game name, print the average wage of the players'''

    # Have the user choose a game 
    game = None
    while game == None:
        game = choose_game(context)

    query = """
    SELECT 
      AVG(Wage) 
    FROM 
      player 
      INNER JOIN employee_data ON employee_data.IdEmployee = player.IdEmployeeData 
      INNER JOIN game ON game.IdGame = player.IdGame 
    WHERE 
      game.Name = :game"""

    par = {"game": game}
    res = context.execute(query, par)
    average_wage = res.fetchall()[0][0]
    print(f"The average wage for {game} players is: ${average_wage}")


def print_tournaments_by_places(context):
    '''Print all tournaments by place'''

    places = get_places(context)
    for place in places:
        print(f"All tournaments for {place[1]}: {place[2]}, {place[3]}")
        tournaments = get_tournaments_by_place(context, place)
        for tournament in tournaments:
            game = get_game_by_id(context, tournament[2])
            date = tournament[3]
            duration = tournament[4]
            print(f"Game: {game} | Date: {date} | Duration: {duration}")
        print()


def print_number_of_players_by_gender(context):
    '''Print the number of players by gender'''

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
    for gender in genders:
        print(f"Total of {gender[0]}: {gender[1]}")


def menu(context):
    functions = {
        1: {
            "desc": "1. List every tournament for a given name",
            "func": print_all_tournaments_for_game,
        },
        2: {
            "desc": "2. Given a game name, retrieve the average wage of the players",
            "func": print_average_wage_for_game,
        },
        3: {
            "desc": "3. List all tournaments by place",
            "func": print_tournaments_by_places,
        },
        4: {
            "desc": "4. Get the number of players by gender",
            "func": print_number_of_players_by_gender,
        },
    }

    # Have the user choose a function
    choice = None
    while choice == None:
        try:
            print("Choose a function:\n")
            for function in functions:
                print(functions[function]["desc"])
            choice = int(input("Choose a function: "))
        except ValueError:
            # If user doesn't enter a number, prints an error message and choice still none
            choice = None

    print()
    try:
        functions[choice]["func"](context)
    except KeyError:
        # If user's choice is not a valid number, re run the menu
        print("Please enter a valid number")
        menu(context)
        return


def main():
    connection = sqlite3.connect("newdb.db")
    context = connection.cursor()
    menu(context)


if __name__ == "__main__":
    main()
