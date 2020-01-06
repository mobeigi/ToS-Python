import townofsalem
from townofsalem.Items import *

tos_client = townofsalem.Client()
res = tos_client.login("username", "password")
tos_client.change_preferences(Character.TEST, House.TEST, Map.TEST, Pet.TEST, LobbyIcon.TEST, DeathAnimation.TEST, Scroll.TEST, Scroll.TEST, Scroll.TEST, "My Name")
tos_client.logout()