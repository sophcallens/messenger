class Channel:
    def __init__(self, id: int, name: str, member_ids: list):
        self.id = id
        self.name = name
        self.member_ids = member_ids
    @classmethod
    def from_dict(cls, channel_dict: dict) -> 'Channel': 
        return cls(channel_dict['id'],channel_dict['name'],channel_dict['member_ids'])

    def to_dict(self : 'Channel') -> 'dict':
        return {'id':self.id, 'name':self.name, 'member_ids': self.member_ids}
