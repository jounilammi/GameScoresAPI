 import requests

BASE_URL="127.0.0.1:5000"
resp = requests.get(BASE_URL + "/api/games/")


def main():


    while True:
        print("Welcome to GameScoresAPI client\n\n")
        print("Do you want to handle?\n")
        print("1. Person")
        print("2. Match")
        print("3 Game")
        print("4 Quit\n")

        menu_sel = input("Type 1, 2 or 3 : ")

        if menu_sel == 1:
            print("You want to?\n")
            print("1. List all persons")
            print("2. Specific person information")
            print("3 Add a person")
            print("4 Edit a person")
            print("5 Delete a person")
            print("6 Previous\n")

        elif menu_sel == 2:

        elif menu_sel == 3:

        elif menu_sel == 4:
            print("Bye")
            break

        else:
            print("Wrong input")

    exit()



def person_menu():
    pass

def match_menu():
    pass

def game_menu():
    pass






def get_persons():
    return requests.get(BASE_URL + "/api/games/")

def get_person():
    return requests.get(BASE_URL + "/api/games/")

def post_person():
    return requests.get(BASE_URL + "/api/games/")

def put_person():
    return requests.get(BASE_URL + "/api/games/")

def delete_person():
    return requests.get(BASE_URL + "/api/games/")




def get_matches():
    return requests.get(BASE_URL + "/api/games/")

def get_match():
    return requests.get(BASE_URL + "/api/games/")

def post_match():
    return requests.get(BASE_URL + "/api/games/")

def put_match():
    return requests.get(BASE_URL + "/api/games/")

def delete_match():
    return requests.get(BASE_URL + "/api/games/")



def get_games():
    return requests.get(BASE_URL + "/api/games/")

def get_game():
    return requests.get(BASE_URL + "/api/games/")

def post_game():
    return requests.get(BASE_URL + "/api/games/")

def put_game():
    return requests.get(BASE_URL + "/api/games/")

def delet_game():
    return requests.get(BASE_URL + "/api/games/")










