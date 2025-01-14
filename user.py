class User:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
    @classmethod
    def from_dict(cls, user_dict: dict) -> 'User': 
        return cls(user_dict['id'],user_dict['name'])

    def to_dict(self) :
        return {'id': self.id, 'name': self.name }