from distutils.command.config import config
import json
from urllib.parse import urldefrag
import requests
from dog.start_status import StartStatus


class DogProxy:
    def __init__(self):
        super().__init__()
        self.dog_actor = None
        self.player_id = 0
        self.player_name = ""
        self.game_id = 0
        self.status = 0
        # 0 - file game.id not found; 1 - not connected to server; 2 - connected without match; 3 - waiting move (even if it's the local player's turn)
        self.move_order = 0
        self.url = "https://api-dog-server.herokuapp.com/"

    def get_status(self):
        return self.status

    def initialize(self, a_name, an_actor):
        self.player_id = self.generate_player_id()
        self.player_name = a_name
        self.dog_actor = an_actor
        if self.player_name == "":
            self.player_name = "player" + str(self.player_id)
        try:
            config_file = open("config/game.id", "r")
            self.game_id = config_file.read()
        except FileNotFoundError:
            self.status = 0
            return "Arquivo de configuração do jogo não encontrado"
        config_file.close()
        resp = self.register_player(self.player_name, self.player_id, self.game_id)
        result = resp.status_code
        if result == 200:
            resp_json = resp.text
            resp_dict = json.loads(resp_json)
            resp1 = resp_dict["0"]
            resp2 = resp_dict["1"]
            self.status = 2
            message = "Conectado a Dog Server"
        else:
            self.status = 1
            message = "Você está sem conexão"
        return message

    def generate_player_id(self):
        from time import time

        milliseconds = int(time() * 1000)
        an_id = str(milliseconds - 1639872000000)
        return an_id

    def register_player(self, a_player_name, a_player_id, a_game_id):
        url = self.url + "player/"
        post_data = {"player_name": a_player_name, "player_id": a_player_id, "game_id": a_game_id}
        resp = requests.post(url, data=post_data)
        return resp

    def start_match(self, number_of_players):
        url = self.url + "start/"
        post_data = {"player_id": self.player_id, "game_id": self.game_id, "number_of_players": number_of_players}
        resp = requests.post(url, data=post_data)
        result = resp.status_code
        if result == 200:
            resp_json = resp.text
            resp_dict = json.loads(resp_json)
            message = resp_dict["message"]
            code = resp_dict["code"]
            players = resp_dict["players"]
            start_status = StartStatus(code, message, players, self.player_id)
            if code == "2":
                self.status = 3
                self.move_order = 0
        else:
            start_status = StartStatus("0", "Voce está offline", [], self.player_id)
        return start_status

    def start_status(self):
        url = self.url + "started/"
        post_data = {"player_id": self.player_id, "game_id": self.game_id}
        resp = requests.post(url, data=post_data)
        result = resp.status_code
        if result == 200 and self.status == 2:
            resp_json = resp.text
            resp_dict = json.loads(resp_json)
            message = resp_dict["message"]
            code = resp_dict["code"]
            players = resp_dict["players"]
            if code == "2":
                start_status = StartStatus(code, message, players, self.player_id)
                self.status = 3
                self.move_order = 0
                self.dog_actor.receive_start(start_status)

    def send_move(self, a_move):
        url = self.url + "move/"
        json_move = json.dumps(a_move)  # convert move to json
        post_data = {"player_id": self.player_id, "game_id": self.game_id, "move": json_move}
        resp = requests.post(url, data=post_data)
        if a_move["match_status"] == "next":
            self.status = 3  #   pass the turn and start looking for a move
        elif a_move["match_status"] == "finished":
            self.status = 2  #   connected without match
        return resp.text

    def match_status(self):
        url = self.url + "match/"
        post_data = {"player_id": self.player_id, "game_id": self.game_id}
        resp = requests.post(url, data=post_data)
        resp_json = resp.text
        seek_result = json.loads(resp_json)
        if bool(seek_result):
            move_dictionary = eval(
                seek_result["1"]
            )  #   move is contained in seek_result as a string (to be converted in dictionary)
            if bool(move_dictionary):
                match_status = move_dictionary["match_status"]
                if match_status == "interrupted":  #  an opponent has abandoned the match
                    self.dog_actor.receive_withdrawal_notification()
                    self.status = 2
                else:
                    move_player_id = move_dictionary["player"]
                    move_player_order = move_dictionary["order"]
                    if move_player_id != str(self.player_id):  #  not from the player himself
                        if int(move_player_order) > self.move_order:  #  not an already handled move
                            self.move_order = int(move_player_order)
                            self.dog_actor.receive_move(move_dictionary)
                            if move_dictionary["match_status"] == "finished":
                                self.status = 2
