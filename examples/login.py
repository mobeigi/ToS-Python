import townofsalem

# Web login with username/password
tos_client = townofsalem.Client()

res = tos_client.login("username", "password")
print(res)

tos_client.logout()

# Steam login with username/password/steamid
tos_client = townofsalem.Client()

res = tos_client.login("username", "password", '76561198108407557')
print(res)

tos_client.logout()
