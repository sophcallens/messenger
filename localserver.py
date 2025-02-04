import json

from datetime import datetime

from server import Server
from user import User
from channel import Channel
from message import Message

class LocalServer(Server) :
    def __init__(self, filename : str):
        self.filename = filename
        self.users : list[User] = []
        self.channels : list[Channel] = []
        self.messages : list[Message] = []


    def load(self) :

        server_dict = json.load(open(self.filename))

        self.users = [User.from_dict(user) for user in server_dict['users']]
        self.channels = [Channel.from_dict(channel) for channel in server_dict['channels']]
        self.messages = [Message.from_dict(message) for message in server_dict['messages']]

    def save(self) : 
        new_server = {
            'users': [user.to_dict() for user in self.users],
            'channels': [channel.to_dict() for channel in self.channels],
            'messages': [message.to_dict() for message in self.messages],
            }

        json.dump(new_server, open(self.filename))
       
    def get_users(self)-> list['User'] :
        return self.users
    
    def get_channels(self) -> list['Channel'] : 
        return self.channels
    
    def get_messages(self,channel_id) -> list['Message'] :
        message_channel = []
        for message in self.messages :
            if str(message.channel) == str(channel_id) :
                message_channel.append(message)
        return message_channel
    
    def add_user(self, name) : 
        self.users.append(User(len(self.users())+1, name))

    def add_channel(self, name : str, login_user : 'User') : 
        self.channels.append(Channel(len(self.channels)+1, name, [login_user.id]))
    
    def add_member(self, channel : Channel, id) :
        channel.member_ids.append(id)
    
    def add_message(self, message, login_user : 'User', channel_id : int):
        self.messages.append(Message(len(self.messages)+1, datetime.now().strftime("%d/%m/%Y %H:%M:%S"), login_user.id, channel_id, message))