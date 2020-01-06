from .Constants import *
from .Authentication import *
from .Functions import *

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

    def login(self, username : str, password: str):
        # Init socket
        self._init_socket()
        return self.auth.login(self._socket, username, password)

    def logout(self):
        return self.auth.logout(self._socket)

    def change_preferences(self, character, house, map, pet, lobby_icon, death_animation, 
        equipped_scroll_1, equipped_scroll_2, equipped_scroll_3, preferred_name):
        Functions.change_preferences(self._socket, character, house, map, pet, lobby_icon, death_animation, 
        equipped_scroll_1, equipped_scroll_2, equipped_scroll_3, preferred_name)

