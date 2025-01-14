import json
import requests

from user import User
from channel import Channel
from message import Message

class Server :
    def __init__(self,file_name : str, users : list['User'],channels: list['Channel'], messages: list['Message']) :
        self.file_name = file_name
        self.users = users
        self.channels = channels
        self.messages = messages

    
    @classmethod
    def filename_to_server(cls,filename) -> 'Server' :

        with open(filename) as json_file :
            server_dict = json.load(json_file)

        users = [User.from_dict(user) for user in server_dict['users']]
        channels = [Channel.from_dict(channel) for channel in server_dict['channels']]
        messages = [Message.from_dict(message) for message in server_dict['messages']]
    

        return Server(filename,users,channels,messages)
    
    @classmethod
    def url_to_server(cls,url) -> 'Server' :
        
        response = requests.get(url)
        server_dict = response.json

        users = [User.from_dict(user) for user in server_dict['users']]
        channels = [Channel.from_dict(channel) for channel in server_dict['channels']]
        messages = [Message.from_dict(message) for message in server_dict['messages']]
    

        return Server(url,users,channels,messages)


