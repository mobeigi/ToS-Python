import json

class LoginMessageWeb():
    RS = b'\x1E'
    NULL = b'\x00'

    def __init__(
        self,
        username : str,
        encrypted_password : str,
        login_type : int,
        platform: int,
        build_id : int,
        steam_id : str = ''
    ):
        self.username = username
        self.encrypted_password = encrypted_password
        self.login_type = login_type
        self.platform = platform
        self.build_id = build_id
    
    @staticmethod
    def from_bytes(bytes):
        return None # TODO

    def __bytes__(self):
        return b'\x02\x02' + bytes([self.login_type]) + bytes([self.platform]) + bytes(str(self.build_id), 'UTF-8') + self.RS + bytes(self.username, 'UTF-8') + self.RS + self.encrypted_password + self.NULL