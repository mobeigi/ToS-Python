import townofsalem
from townofsalem.Items import *

tos_client = townofsalem.Client()
res = tos_client.login("username", "password")
tos_client.stir_daily_brew()
tos_client.logout()