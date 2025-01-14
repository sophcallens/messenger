import json

from server import Server
from user import User
from channel import Channel
from message import Message

class LocalServer(Server) :
    def __init__(self, filename : str):
        self.filename = filename
        self.users : list[User] = []
        self.channels : list[Channel] = []
        self.message : list[Message] = []


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
       
