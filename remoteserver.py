from server import Server
from user import User
from channel import Channel
from message import Message

class RemoteServer(Server) :
    def __init__(self, filename : str):
        self._filename = filename
        self._users : list[User] = []
        self._channels : list[Channel] = []
        self._message : list[Message] = []

    @override
    def load(self) :
        



