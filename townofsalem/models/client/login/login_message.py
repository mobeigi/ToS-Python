import json

class LoginMessage():
    def __init__(
        self,
        username : str,
        password : str,
        login_type : int,
        platform: int,
        build_id : int,
        steam_id : str = ''
    ):
        self.username = username
        self.password = password
        self.login_type = login_type
        self.platform = platform
        self.build_id = build_id
        self.steam_id = steam_id
    
    @staticmethod
    def from_bytes(bytes):
        return None # TODO

    def __bytes__(self):
        return bytes(json.dumps({'username': self.username,'password':self.password,'type':self.login_type,'platform': self.platform,'build_id':self.build_id,'steam_id':self.steam_id}), 'UTF-8')