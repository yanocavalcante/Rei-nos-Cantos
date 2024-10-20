from dog.dog_proxy import DogProxy
from dog.polling_thread import PollingThread


class DogActor:
    def __init__(self):
        super().__init__()
        self.proxy = DogProxy()
        self.player_actor = None
        self.polling_thread = PollingThread(self.proxy, True)

    def initialize(self, player_name, a_player_actor):
        self.player_actor = a_player_actor
        resp_dict = self.proxy.initialize(player_name, self)
        self.polling_thread.start()
        return resp_dict

    def start_match(self, number_of_players):
        return self.proxy.start_match(number_of_players)

    def send_move(self, move):
        self.proxy.send_move(move)

    def receive_start(self, start_status):
        self.player_actor.receive_start(start_status)

    def receive_move(self, a_move):
        self.player_actor.receive_move(a_move)

    def receive_withdrawal_notification(self):
        self.player_actor.receive_withdrawal_notification()
