from .constants import NULL
from .models.client.login_type import LoginType
from .models.client.platform import Platform
from .models.client.message_type import MessageType
from .models.client.login.login_message import LoginMessage
from .models.client.login.login_message_web import LoginMessageWeb
from .models.login_status import LoginStatus

import json
from enum import IntEnum
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from Crypto.Cipher import AES
from base64 import b64decode, b64encode

class Authentication():
    DEFAULT_HOST = 'live4.tos.blankmediagames.com'
    DEFAULT_PORT = 3600
    DEFAULT_BUILD_ID = 12587
    DEFAULT_PUB_KEY = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAziIxzMIz7ZX4KG5317SmVeCt9SYIe/+qL3hqP5NUX0i1iTmD7x9hFR8YoOHdAqdCJ3dxi3npkIsO6Eoz0l3eH7R99DX16vbnBCyvA3Hkb1B/0nBwOe6mCq73vBdRgfHU8TOF9KtUOx5CVqR50U7MtKqqc6M19OZXZuZSDlGLfiboY99YV2uH3dXysFhzexCZWpmA443eV5ismvj3NyxvRk/4ushZV50vrDjYiInNEj4ICbTNXQULFs6Aahmt6qmibEC6bRl0S4TZRtzuk2a3TpinLJooDTt9s5BvRRh8DLFZWrkWojgrzS0sSNcNzPAXYFyTOYEovWWKW7TgUYfAdwIDAQAB'

    def __init__(
        self,
        host : str = DEFAULT_HOST,
        port : int = DEFAULT_PORT,
        build_id : int = DEFAULT_BUILD_ID,
        pub_key : str = DEFAULT_PUB_KEY
    ):
        self.host = host
        self.port = port
        self.build_id = build_id
        self.pub_key = pub_key

    def _encrypt_with_public_key(self, data):
        decoded_pub_key = RSA.importKey(b64decode(self.pub_key))
        signer = Cipher_PKCS1_v1_5.new(decoded_pub_key)
        encrypted_data = signer.encrypt(data)
        return encrypted_data
    
    def _pad(self, s, b):
        return s + (b - len(s) % b) * chr(b - len(s) % b)

    def _login_web(self, socket, username, password):
        # Encrypt password
        encrypted_password = b64encode(self._encrypt_with_public_key(bytes(password, 'UTF-8')))
        packet = bytes(LoginMessageWeb(username, encrypted_password, LoginType.Web, Platform.WEB, self.build_id))
        
        # Send Packet
        socket.send(packet)        
        data = socket.recv(3)
        login_status = LoginStatus(int(data[1])-1)

        if login_status == LoginStatus.Authenticating:
            # Post login data
            data = socket.recv(2048)

        return login_status

    def _login_steam(self, socket, username, password, steamid):
        payload = bytes(LoginMessage(username, password, LoginType.SteamUsernamePassword, Platform.STEAM, self.build_id, steamid))

        # Generate random AES key and iv
        random = Random.new()
        key = random.read(32)
        iv = random.read(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)

        # Encrypt payload using AES
        payload = bytes(self._pad(payload.decode('UTF-8'), 16), 'UTF-8')
        payload = cipher.encrypt(payload)

        # Encrypt key using public key
        encrypted_key = self._encrypt_with_public_key(key)

        # base64 encode all data
        encrypted_key = b64encode(encrypted_key)
        iv = b64encode(iv)
        payload = b64encode(payload)

        packet = bytes([MessageType.Login]) + bytes(json.dumps({'key':encrypted_key.decode('UTF-8'),'iv':iv.decode('UTF-8'),'payload':payload.decode('UTF-8')}), 'UTF-8') + NULL
        
        # Send Packet
        socket.send(packet)
        data = socket.recv(3)
        login_status = LoginStatus(int(data[1])-1)

        if login_status == LoginStatus.Authenticating:
            # Post login data
            data = socket.recv(2048)

        return login_status

    def login(self, socket, username, password, steamid = None):
        if steamid is not None:
            return self._login_steam(socket, username, password, steamid)
        else:
            return self._login_web(socket, username, password)

    def logout(self, socket):
        # Send FIN bit
        socket.shutdown(1)
        socket.recv(0) # Empty packet FIN ACK
        return True