import requests
import json
from datetime import datetime


from server import Server
from user import User
from channel import Channel
from message import Message

class RemoteServer(Server) :
    def __init__(self, filename : str):
        self.filename = filename
        self.users : list[User] = []
        self.channels : list[Channel] = []
        self.message : list[Message] = []

    def load(self) :
        pass

    def save(slef) :
        pass

    def get_users(self) -> list['User'] :
        response = (requests.get(self.filename+'/users'))
        response.raise_for_status()
        return [User(user['id'],user['name'],) for user in response.json()]

    def get_channels(self) -> list['Channel'] :
        response = requests.get(self.filename+'/channels')
        return [Channel(channel['id'],channel['name'],[]) for channel in response.json()]
    
    def get_messages(self, channel_id) -> list['Message'] :
        response = requests.get(f'{self.filename}/channels/{channel_id}/massages')
        return [Message(message['id'], message['reception_date'],message['sender_id'],message['channel_id'],message['content']) for message in response.json()]
    
    def add_user(self, name) : 
        requests.post(self.filename + '/users/create', json= {'name': name})
        
    def add_channel(self, name : str, login_user : 'User') : 
        requests.post(self.filename + '/channels/create', json= {'name': name})
        for channel in self.get_channels():
            if channel.name == name :
                self.add_member(channel, login_user.id)
    
    def add_member(self, channel : Channel, id) :
        print(f"{channel.id}{id}")
        requests.post(f'{self.filename}/channels/{channel.id}/join', json= {'user_id': id})

    def add_message(self, message, login_user : 'User', channel_id : int):
        requests.post(self.filename +'/channels/messages', json= {'content':message, 'reception_date':datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'sender_id':login_user.id,'channel_id':channel_id})