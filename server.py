import json
import requests

from user import User
from channel import Channel
from message import Message

class Server :
    def __init__(self,filename : str, users : list['User'],channels: list['Channel'], messages: list['Message']) :
        self.filename = filename
        self.users = users
        self.channels = channels
        self.messages = messages

    

