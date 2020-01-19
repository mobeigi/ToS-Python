from .constants import *

class Functions():

    # Change preferrences that are stored server side
    @staticmethod
    def change_preferences(socket, character, house, map, pet, lobby_icon, death_animation, 
        equipped_scroll_1, equipped_scroll_2, equipped_scroll_3, preferred_name):
        packet = b'\x14' + \
            character + COMMA + \
            house + COMMA + \
            map + COMMA + \
            pet + COMMA + \
            lobby_icon + COMMA + \
            death_animation + COMMA + \
            equipped_scroll_1 + COMMA + \
            equipped_scroll_2 + COMMA + \
            equipped_scroll_3 + COMMA + \
            bytes(preferred_name, 'UTF-8') + \
            NULL
        
        socket.send(packet)
        data = socket.recv(0) # Empty packet ACK
        return True

    @staticmethod
    def join_queue(socket):
        packet = b'\x7f' + NULL
        socket.send(packet)
        data = socket.recv(0) # Receive ACK
        
        packet = b'\x3c\x06\x00'
        socket.send(packet)
        data = socket.recv(6)
        
        seconds_till_queue_pop = int(data[2:].decode('ascii').rstrip('\x00'))
        return seconds_till_queue_pop

    @staticmethod
    def leave_queue(socket):
        packet = b'\x3d' + NULL
        socket.send(packet)
        data = socket.recv(2)
            
        if data == b'\x48\x00':
            return True
        else:
            return False

    @staticmethod
    def buy_item(socket, currency, item_id, quantity):

        # Sent before buy item packet
        packet = b'\x7f' + NULL
        socket.send(packet)
        data = socket.recv(0) # Receive ACK
        
        packet = b'\x4a' + bytes(str(currency.value), 'UTF-8') + bytes(item_id, 'UTF-8') + COMMA + bytes(str(quantity), 'UTF-8') + NULL
        socket.send(packet)
        
        data = socket.recv(1024) # TODO