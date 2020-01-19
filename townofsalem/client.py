from .items import Special
from .authentication import Authentication
from .functions import Functions
from .models.currency_type import CurrencyType

import socket

class Client():
    
    def __init__(
        self,
        auth : Authentication = Authentication()
    ):
        """Instantiates a new Client."""
        self.auth = auth
        self._socket = None
    
    def _init_socket(self):
        if self._socket is None:
            self._socket = socket.socket()
            self._socket.connect((self.auth.host, self.auth.port))

    def login(self, username : str, password: str, steamid: str = None):
        # Init socket
        self._init_socket()
        return self.auth.login(self._socket, username, password, steamid)

    def logout(self):
        return self.auth.logout(self._socket)

    def change_preferences(self, character, house, map, pet, lobby_icon, death_animation, 
        equipped_scroll_1, equipped_scroll_2, equipped_scroll_3, preferred_name):
        Functions.change_preferences(self._socket, character, house, map, pet, lobby_icon, death_animation, 
        equipped_scroll_1, equipped_scroll_2, equipped_scroll_3, preferred_name)

    def join_queue(self):
        return Functions.join_queue(self._socket)

    def leave_queue(self):
        return Functions.leave_queue(self._socket)

    def buy_item(self, currency, item_id, quantity):
        Functions.buy_item(self._socket, currency, item_id, quantity)

    def stir_daily_brew(self):
        # Implemented as buying an item
        Functions.buy_item(self._socket, CurrencyType.TownPoints, Special.DAILY_BREW, 1)