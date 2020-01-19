import json

class LoginSteamWithUsernameMessage():
    def __init__(
        self,
        steam_id: str,
        username : str,
        password : str,
        login_type : int,
        platform: int,
        build_id : int
    ):
        self.steam_id = steam_id
        self.username = username
        self.password = password
        self.login_type = login_type
        self.platform = platform
        self.build_id = build_id
    
    @staticmethod
    def from_bytes(bytes):
        return None # TODO

    def __bytes__(self):
        return bytes(json.dumps({'steam_id':self.steam_id,'username': self.username,'password':self.password,'type':self.login_type,'platform': self.platform,'build_id':self.build_id}), 'UTF-8')