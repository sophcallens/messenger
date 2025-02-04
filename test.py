import requests

filename = 'https://groupe5-python-mines.fr'
channel_id = 15
id = 27
requests.post(filename + f'/channels/{channel_id}/join', json= {'user_id': id})