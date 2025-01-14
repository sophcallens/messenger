class Message:
    def __init__(self, id: int, reception_date: str, sender_id: int, channel: int,content:str ):
        self.id = id
        self.reception_date = reception_date
        self.sender_id = sender_id
        self.channel = channel
        self.content = content
    @classmethod
    def from_dict(cls, message_dict : dict) -> 'Message' :
        return cls(message_dict['id'],message_dict['reception_date'],message_dict['sender_id'],message_dict['channel'],message_dict['content'])

    def to_dict(self) :
        return {'id':self.id,'reception_date':self.reception_date,'sender_id':self.sender_id,'channel':self.channel,'content':self.content}
