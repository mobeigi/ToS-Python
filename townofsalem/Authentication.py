from .Constants import *

from enum import IntEnum
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from base64 import b64decode, b64encode

class LoginResponse(IntEnum):
    LOGIN_SUCCESS  = 1
    LOGIN_FAILED = 2
    LOGIN_BANNED = 3
    LOGIN_PASSWORD_CHANGE_REQUIRED = 4
    UNKNOWN_RESPONSE = 5

class Authentication():
    DEFAULT_HOST = 'live4.tos.blankmediagames.com'
    DEFAULT_PORT = 3600
    DEFAULT_BUILD_ID = 11704
    DEFAULT_PUB_KEY = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAziIxzMIz7ZX4KG5317Sm\nVeCt9SYIe/+qL3hqP5NUX0i1iTmD7x9hFR8YoOHdAqdCJ3dxi3npkIsO6Eoz0l3e\nH7R99DX16vbnBCyvA3Hkb1B/0nBwOe6mCq73vBdRgfHU8TOF9KtUOx5CVqR50U7M\ntKqqc6M19OZXZuZSDlGLfiboY99YV2uH3dXysFhzexCZWpmA443eV5ismvj3Nyxv\nRk/4ushZV50vrDjYiInNEj4ICbTNXQULFs6Aahmt6qmibEC6bRl0S4TZRtzuk2a3\nTpinLJooDTt9s5BvRRh8DLFZWrkWojgrzS0sSNcNzPAXYFyTOYEovWWKW7TgUYfA\ndwIDAQAB'

    def __init__(
        self,
        host : str = DEFAULT_HOST,
        port : int = DEFAULT_PORT,
        build_id : int = DEFAULT_BUILD_ID,
        pub_key : str = DEFAULT_PUB_KEY
    ):
        self.host = host
        self.port = port
        self.build_id = bytes(str(build_id), 'UTF-8')
        self.pub_key = pub_key

    def _encrypt_password(self, password):
        decoded_pub_key = RSA.importKey(b64decode(self.pub_key))
        signer = Cipher_PKCS1_v1_5.new(decoded_pub_key)
        signature = signer.encrypt(password.encode())
        return b64encode(signature)

    # Authenticate with server
    def login(self, socket, username, password):
        encrypted_password = self._encrypt_password(password)
        packet = b'\x02\x02\x02\x01' + self.build_id + RS + bytes(username, 'UTF-8') + RS + encrypted_password + NULL
        socket.send(packet)
        data = socket.recv(3)
        if data == b'\x01\x02\x00':
            # Post login data
            data = socket.recv(2048)
            return LoginResponse.LOGIN_SUCCESS
        elif data == b'\xe2\x03\x00':
            return LoginResponse.LOGIN_FAILED
        elif data == b'\xa2\x07\x01':
            return LoginResponse.LOGIN_BANNED
        elif data == b'\xa2\x0e\x00':
            return LoginResponse.LOGIN_PASSWORD_CHANGE_REQUIRED
        else:
            return LoginResponse.UNKNOWN_RESPONSE

    def logout(self, socket):
        # Send FIN bit
        socket.shutdown(1)
        data = socket.recv(0) # Empty packet FIN ACK
        return True