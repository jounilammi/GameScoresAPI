import requests
import sys
import json
import datetime

BASE_URL = "http://127.0.0.1:5000"


def main():

    while True:

        menu_sel = int(main_menu())
        if menu_sel not in [1, 2, 3, 4]:
            print("Wrong input")
            continue
        func_sel = menu_page_2(menu_sel)

        request(menu_sel, func_sel)

    exit()


# MENU FUNCTIONS#
def main_menu():

    while True:
        print("\n----------------------------------------------------------------------\n")
        print("Welcome to GameScoresAPI client\n\n")
        print("Do you want to handle?\n")
        print("1. Person")
        print("2. Match")
        print("3. Game")
        print("4. Quit\n")

        menu_sel = int(input("Type 1, 2, 3 or 4: "))
        if menu_sel == "":
            print("Wrong input")
            continue
        return menu_sel


def menu_page_2(menu_sel):

    if menu_sel == 1:
        print("\nYou want to?\n")
        print("1. List all persons")
        print("2. Specific person information")
        print("3. Add a person")
        print("4. Edit a person")
        print("5. Delete a person")
        print("6. Previous\n")
        sel = int(input("Type 1, 2, 3, 4, 5 or 6: "))
        print()

    elif menu_sel == 2:
        print("\nYou want to?\n")
        print("1. List all matches")
        print("2. Specific match information")
        print("3. Add a match")
        print("4. Edit a match")
        print("5. Delete a match")
        print("6. Previous\n")
        sel = int(input("Type 1, 2, 3, 4, 5 or 6: "))
        print()

    elif menu_sel == 3:
        print("\nYou want to?\n")
        print("1. List all games")
        print("2. Specific game information")
        print("3. Add a game")
        print("4. Edit a game")
        print("5. Delete a game")
        print("6. Previous\n")
        sel = int(input("Type 1, 2, 3, 4, 5 or 6: "))
        print()

    elif menu_sel == 4:
        print("Bye!")
        sys.exit(0)

    else:
        print("Wrong input")

    return sel


def request(menu_sel, func_sel):

    # Person
    if menu_sel == 1 and func_sel == 1:
        get_persons()
        main()
    elif menu_sel == 1 and func_sel == 2:
        get_person()
        main()
    elif menu_sel == 1 and func_sel == 3:
        post_person()
        main()
    elif menu_sel == 1 and func_sel == 4:
        put_person()
        main()
    elif menu_sel == 1 and func_sel == 5:
        delete_person()
        main()
    elif menu_sel == 1 and func_sel == 6:
        main()

    # Match
    if menu_sel == 2 and func_sel == 1:
        game_id = input("Give id of the game, which matches you want to see: ")
        get_matches(game_id)
        main()
    elif menu_sel == 2 and func_sel == 2:
        game_id = input("Give id of the game, which matches you want to see: ")
        get_match(game_id)
        main()
    elif menu_sel == 2 and func_sel == 3:
        game_id = input("Give id of the game, which match you want to post: ")
        post_match(game_id)
        main()
    elif menu_sel == 2 and func_sel == 4:
        game_id = input("Give id of the game, which match you want to put: ")
        put_match(game_id)
        main()
    elif menu_sel == 2 and func_sel == 5:
        game_id = input("Give id of the game, which match you want to delete: ")
        delete_match(game_id)
        main()
    elif menu_sel == 2 and func_sel == 6:
        main()

    # Game
    if menu_sel == 3 and func_sel == 1:
        get_games()
        main()
    elif menu_sel == 3 and func_sel == 2:
        get_game()
        main()
    elif menu_sel == 3 and func_sel == 3:
        post_game()
        main()
    elif menu_sel == 3 and func_sel == 4:
        put_game()
        main()
    elif menu_sel == 3 and func_sel == 5:
        delete_game()
        main()
    elif menu_sel == 3 and func_sel == 6:
        main()


#################
# PERSON REQUESTS#
#################

def get_persons():
    resp = requests.get(BASE_URL + "/api/persons/")
    body = resp.json()
    for item in body["items"]:
        print("Id: "+str(item["id"]))
        print("username: "+str(item["username"]))
        print("first name: "+str(item["first_name"]))
        print("last name: "+str(item["last_name"]))
        print("birthdate: "+str(item["birthdate"]))
        print("description: "+str(item["description"]))
        print("--------------\n")
    return


def get_person():
    while True:
        input_id = input("Give person id: ")
        if not input_id:
            print("Id can't be null")
            continue
        break

    url = BASE_URL + "/api/persons/{}/".format(input_id)

    resp = requests.get(url)
    body = resp.json()
    print("Id: "+str(body["id"]))
    print("username: "+str(body["username"]))
    print("first name: "+str(body["first_name"]))
    print("last name: "+str(body["last_name"]))
    print("birthdate: "+str(body["birthdate"]))
    print("description: "+str(body["description"]))
    return


def post_person():
    data = {}

    while True:
        input_username = input("Give person username: ")
        if not input_username:
            print("Username can't be null")
            continue
        data["username"] = input_username
        break

    while True:
        input_first_name = input("Give person first name: ")
        if not input_first_name:
            print("First name can't be null")
            continue
        data["first_name"] = input_first_name
        break

    while True:
        input_last_name = input("Give person last name: ")
        if not input_last_name:
            print("Last name can't be null")
            continue
        data["last_name"] = input_last_name
        break

    input_birthdate = "1900-1-1"
    while True:
        print("The person's birthday: just press enter when year is prompt if")
        print("you don't want to give birthdate")

        year = input("Enter year: ")
        if year == "":
            break
        month = input("Enter month: ")
        day = input("Enter day: ")
        try:
            datetime.datetime(year=int(year), month=int(month), day=int(day))
        except Exception:
            print("Date was not legit, try again")
            continue
        input_birthdate = year+"-"+month+"-"+day
        break

    data["birthdate"] = input_birthdate
    data["description"] = input("Give custom description (optional): ")
    print(data)
    return requests.post(BASE_URL + "/api/persons/", data=json.dumps(data),
                         headers={"Content-type": "application/json"}
    )


def put_person():
    data = {}
    while True:
        input_id = input("Give person id: ")
        if not input_id:
            print("Id can't be null")
            continue
        break

    while True:
        input_username = input("Give person username: ")
        if not input_username:
            print("Username can't be null")
            continue
        data["username"] = input_username
        break

    while True:
        input_first_name = input("Give person first name: ")
        if not input_first_name:
            print("First name can't be null")
            continue
        data["first_name"] = input_first_name
        break

    while True:
        input_last_name = input("Give person last name: ")
        if not input_last_name:
            print("Last name can't be null")
            continue
        data["last_name"] = input_last_name
        break

    input_birthdate = "1900-1-1"
    while True:
        print("The person's birthday: just press enter when year is prompt if")
        print("you don't want to give birthdate")

        year = input("Enter year: ")
        if year == "":
            break
        month = input("Enter month: ")
        day = input("Enter day: ")
        try:
            datetime.datetime(year=int(year), month=int(month), day=int(day))
        except Exception:
            print("Date was not legit, try again")
            continue
        input_birthdate = year+"-"+month+"-"+day
        break
    data["birthdate"] = input_birthdate
    data["description"] = input("Give custom description (optional): ")

    return requests.put(BASE_URL + "/api/persons/{}/".format(input_id), data=json.dumps(data),
                        headers={"Content-type": "application/json"})


def delete_person():
    while True:
        input_id = input("Give person id: ")
        if not input_id:
            print("Id can't be null")
            continue
        break

    return requests.delete(BASE_URL + "/api/persons/{}/".format(input_id))


################
# MATCH REQUESTS#
################

def get_matches(game_id):
    resp = requests.get(BASE_URL + "/api/games/{}/matches/".format(game_id))
    body = resp.json()
    for item in body["items"]:
        print("Id: "+str(item["id"]))
        print("game: "+str(item["game"]))
        print("place: "+str(item["place"]))
        print("time: "+str(item["time"]))
        print("player1_id: "+str(item["player1_id"]))
        print("player2_id: "+str(item["player2_id"]))
        print("player1_score: "+str(item["player1_score"]))
        print("player2_score: "+str(item["player2_score"]))
        print("Comment: "+str(item["comment"]))
        print("--------------\n")
    return


def get_match(game_id):

    data = {}
    while True:
        input_id = input("Give match id: ")
        if not input_id:
            print("Id can't be null")
            continue
        data["id"] = input_id
        break

    url = BASE_URL + "/api/games/{}/matches/{}/".format(game_id, input_id)
    resp = requests.get(url)
    body = resp.json()
    print("Id: "+str(body["id"]))
    print("place: "+str(body["place"]))
    print("time: "+str(body["time"]))
    print("player 1 id: "+str(body["player1_id"]))
    print("player 2 id: "+str(body["player2_id"]))
    print("player 1 score: "+str(body["player1_score"]))
    print("player 2 score: "+str(body["player2_score"]))
    print("comment: "+str(body["comment"]))
    return


def post_match(game_id):

    data = {}
    data["game"] = int(game_id)
    while True:
        input_player1_score = input("Give player 1 score: ")
        if not input_player1_score:
            print("Player 1 score can't be null")
            continue
        data["player1_score"] = float(input_player1_score)
        break

    while True:
        input_player2_score = input("Give player 2 score: ")
        if not input_player2_score:
            print("player 2 score can't be null")
            continue
        data["player2_score"] = float(input_player2_score)
        break

    input_place = input("Give the place the match happened(optional): ")
    data["place"] = input_place

    input_time = "1900-1-1-0-0"
    while True:
        print("The time of the match: just press enter when year is prompt if")
        print("you don't want to give the time")

        year = input("Enter year: ")
        if year == "":
            break
        month = input("Enter month: ")
        day = input("Enter day: ")
        hour = input("Enter hour: ")
        minute = input("Enter minute: ")
        try:
            datetime.datetime(
                year=int(year),
                month=int(month),
                day=int(day),
                hour=int(hour),
                minute=int(minute)
            )
        except Exception:
            print("Date was not legit, try again")
            continue
        input_time = year+"-"+month+"-"+day+"-"+hour+"-"+minute
        break

    data["time"] = input_time

    input_player1_id = input("Give person 1 id: ")
    data["player1_id"] = int(input_player1_id)

    input_player2_id = input("Give person 2 id: ")
    data["player2_id"] = int(input_player2_id)

    input_comment = input("Comment(optional): ")
    data["comment"] = input_comment

    return requests.post(BASE_URL + "/api/games/{}/matches/".format(game_id), data=json.dumps(data),
                         headers={"Content-type": "application/json"})


def put_match(game_id):
    data = {}
    data["game"] = int(game_id)
    while True:
        input_id = input("Give match id: ")
        if not input_id:
            print("Id can't be null")
            continue
        break

    while True:
        input_player1_score = input("Give player 1 score: ")
        if not input_player1_score:
            print("Player 1 score can't be null")
            continue
        data["player1_score"] = int(input_player1_score)
        break

    while True:
        input_player2_score = input("Give player 2 score: ")
        if not input_player2_score:
            print("player 2 score can't be null")
            continue
        data["player2_score"] = int(input_player2_score)
        break

    input_place = input("Give the place the match happened(optional): ")
    data["place"] = input_place

    input_time = "1900-1-1-0-0"
    while True:
        print("The time of the match: just press enter when year is prompt if")
        print("you don't want to give the time")

        year = input("Enter year: ")
        if year == "":
            break
        month = input("Enter month: ")
        day = input("Enter day: ")
        hour = input("Enter hour: ")
        minute = input("Enter minute: ")
        try:
            datetime.datetime(
                year=int(year),
                month=int(month),
                day=int(day),
                hour=int(hour),
                minute=int(minute)
            )
        except Exception:
            print("Date was not legit, try again")
            continue
        input_time = year+"-"+month+"-"+day+"-"+hour+"-"+minute
        break
    data["time"] = input_time

    input_player1_id = input("Give person 1 id: ")
    data["player1_id"] = int(input_player1_id)

    input_player2_id = input("Give person 2 id: ")
    data["player2_id"] = int(input_player2_id)

    input_comment = input("Comment(optional): ")
    data["comment"] = input_comment

    return requests.put(BASE_URL + "/api/games/{}/matches/{}/".format(game_id,input_id), data=json.dumps(data),
                         headers={"Content-type": "application/json"})


def delete_match(game_id):

    while True:
        input_id = input("Give match id: ")
        if not input_id:
            print("Id can't be null")
            continue
        break

    return requests.delete(BASE_URL + "/api/games/{}/matches/{}/".format(game_id,input_id))

###############
# GAME REQUESTS#
###############


def get_games():
    resp = requests.get(BASE_URL + "/api/games/")
    body = resp.json()
    for item in body["items"]:
        print("Id: "+str(item["id"]))
        print("name: "+str(item["name"]))
        print("score type: "+str(item["score_type"]))
        print("--------------\n")
    return


def get_game():
    data = {}
    while True:
        input_id = input("Give game id: ")
        if not input_id:
            print("Id can't be null")
            continue
        data["id"] = input_id
        break

    url = BASE_URL + "/api/games/{}/".format(input_id)

    resp = requests.get(url)
    body = resp.json()
    print("Id: "+str(body["id"]))
    print("Name: "+str(body["name"]))
    print("Score type: "+str(body["score_type"]))
    return


def post_game():
    data = {}
    while True:
        input_name = input("Give name of the game: ")
        if not input_name:
            print("Name can't be null")
            continue
        data["name"] = input_name
        break

    while True:
        input_score_type = input("Give games score type: ")
        if not input_score_type:
            print("Score type can't be null")
            continue
        data["score_type"] = int(input_score_type)
        break

    return requests.post(BASE_URL + "/api/games/", data=json.dumps(data), headers={"Content-type": "application/json"})


def put_game():
    data = {}
    while True:
        input_id = input("Give game id: ")
        if not input_id:
            print("Id can't be null")
            continue
        break

    while True:
        input_name = input("Give name of the game: ")
        if not input_name:
            print("Name can't be null")
            continue
        data["name"] = input_name
        break

    while True:
        input_score_type = input("Give games score type: ")
        if not input_score_type:
            print("Score type can't be null")
            continue
        data["score_type"] = int(input_score_type)
        break
    return requests.put(BASE_URL + "/api/games/{}/".format(input_id), data=json.dumps(data), headers={"Content-type": "application/json"})


def delete_game():
    while True:
        input_id = input("Give game id: ")
        if not input_id:
            print("Id can't be null")
            continue
        break

    return requests.delete(BASE_URL + "/api/games/{}/".format(input_id))


main()

