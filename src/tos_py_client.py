#!/usr/bin/env python

# 
# TOS Python Client
# 

import socket

from time import sleep

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from base64 import b64decode, b64encode

from enum import IntEnum

class LoginResponse(IntEnum):
    LOGIN_SUCCESS  = 1
    LOGIN_FAILED = 2
    LOGIN_BANNED = 3
    LOGIN_PASSWORD_CHANGE_REQUIRED = 4
    UNKNOWN_RESPONSE = 5

class Currency(IntEnum):
    TOWN_POINTS = 1
    STEAM_WALLET = 2
    MERIT_POINTS = 3
    

BMG_PUBKEY = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAziIxzMIz7ZX4KG5317Sm\nVeCt9SYIe/+qL3hqP5NUX0i1iTmD7x9hFR8YoOHdAqdCJ3dxi3npkIsO6Eoz0l3e\nH7R99DX16vbnBCyvA3Hkb1B/0nBwOe6mCq73vBdRgfHU8TOF9KtUOx5CVqR50U7M\ntKqqc6M19OZXZuZSDlGLfiboY99YV2uH3dXysFhzexCZWpmA443eV5ismvj3Nyxv\nRk/4ushZV50vrDjYiInNEj4ICbTNXQULFs6Aahmt6qmibEC6bRl0S4TZRtzuk2a3\nTpinLJooDTt9s5BvRRh8DLFZWrkWojgrzS0sSNcNzPAXYFyTOYEovWWKW7TgUYfA\ndwIDAQAB'

TOS_HOST = 'live4.tos.blankmediagames.com' # 104.239.149.6
TOS_PORT = 3600
TOS_BUILD_ID = bytes('11704', 'UTF-8')

RS = b'\x1E' # Record Seperator ASCII Code 30
NULL = b'\x00'
COMMA = b'\x2C'

def encrypt_password(password):
    pub_key = RSA.importKey(b64decode(BMG_PUBKEY))
    signer = Cipher_PKCS1_v1_5.new(pub_key)
    signature = signer.encrypt(password.encode())
    return b64encode(signature)

# Authenticate with server
def login(tos_socket, username, password):
    encrypted_password = encrypt_password(password)
    packet = b'\x02\x02\x02\x01' + TOS_BUILD_ID + RS + bytes(username, 'UTF-8') + RS + encrypted_password + NULL
    tos_socket.send(packet)
    data = tos_socket.recv(3)
    
    if data == b'\x01\x02\x00':
        # Post login data
        data = tos_socket.recv(2048)
        return LoginResponse.LOGIN_SUCCESS
    elif data == b'\xe2\x03\x00':
        return LoginResponse.LOGIN_FAILED
    elif data == b'\xa2\x07\x01':
        return LoginResponse.LOGIN_BANNED
    elif data == b'\xa2\x0e\x00':
        return LoginResponse.LOGIN_PASSWORD_CHANGE_REQUIRED
    else:
        return LoginResponse.UNKNOWN_RESPONSE

def logout(tos_socket):
    # Send FIN bit
    tos_socket.shutdown(1)
    data = tos_socket.recv(0) # Empty packet FIN ACK
    return True

# Change preferrences that are stored server side
def change_preferences(tos_socket, preferred_name):
    # Character, House, Map, Pet, Lobby Icon, Death Anim, Eq Scroll 1, 2, 3, Pref Name
    packet = b'\x14' + \
        b'\x33\x33' + COMMA + \
        b'\x30' + COMMA + \
        b'\x30' + COMMA + \
        b'\x32' + COMMA + \
        b'\x30' + COMMA + \
        b'\x2d\x30' + COMMA + \
        b'\x32\x33' + COMMA + \
        b'\x32\x34' + COMMA + \
        b'\x32\x35' + COMMA + \
        bytes(preferred_name, 'UTF-8') + \
        NULL
    
    tos_socket.send(packet)
    data = tos_socket.recv(0) # Empty packet ACK
    return True

def join_queue():
    packet = b'\x7f' + NULL
    tos_socket.send(packet)
    data = tos_socket.recv(0) # Receive ACK
    
    packet = b'\x3c\x06\x00'
    tos_socket.send(packet)
    data = tos_socket.recv(6)
    
    seconds_till_queue_pop = int(data[2:].decode('ascii').rstrip('\x00'))
    return seconds_till_queue_pop

def leave_queue():
    packet = b'\x3d' + NULL
    tos_socket.send(packet)
    data = tos_socket.recv(2) # 48 00
        
    if data == b'\x48\x00':
        return True
    else:
        return False

def buy_item(currency, item_id, quantity):

    # Sent before buy item packet
    packet = b'\x7f' + NULL
    tos_socket.send(packet)
    data = tos_socket.recv(0) # Receive ACK
    
    packet = b'\x4a' + bytes(str(currency), 'UTF-8') + bytes(item_id, 'UTF-8') + COMMA + bytes(str(quantity), 'UTF-8') + NULL
    tos_socket.send(packet)
    
    data = tos_socket.recv(1024) # TODO

if __name__ == "__main__":
    
    tos_socket = socket.socket()
    tos_socket.connect((TOS_HOST, TOS_PORT))
    res = login(tos_socket, 'Username', 'Password')
    
    
    logout(tos_socket)
    tos_socket.close()
