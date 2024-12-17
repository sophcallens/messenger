from datetime import datetime
import json

class User:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

class Channel:
    def __init__(self, id: int, name: str, member_ids: list):
        self.id = id
        self.name = name
        self.member_ids = member_ids

class Message:
    def __init__(self, id: int, reception_date: str, sender_id: int, channel: int,content:str ):
        self.id = id
        self.reception_date = reception_date
        self.sender_id = sender_id
        self.channel = channel
        self.content = content

server_file_name = 'server-data.json'

def load_server():
    with open(server_file_name) as json_file :
        server = json.load(json_file)
    return server

server = load_server()

username = None

def identification() :
    global username 
    username = input('x. Exit \n\nusername : ')
    if username in {user['name'] for user in server['users']} :
        print('\n-> Welcome',username,'!')
        menu_principal()
    elif username == 'x' :
        save(server)
        print('\n-> Bye! \n')
    else : 
        print('/!\ Unknown username :', username,'\n')
        identification()

def menu_principal():

    print ('')
    print('=== Menu principal === \n')
    print('1. See users')
    print('2. See channels \n')
    print('x. Save and Exit \n')

    choice = input('Select an option: ')

    if choice == 'x':
        save(server)
        print('\n-> Bye! \n')
    elif choice == '1' :
        users()
    elif choice == '2' :
        channels()   
    else:
        print('Unknown option:', choice)
        menu_principal()

def new_name() :
    new_name = input('\nNew Name :')
    server['users'].append({'id':len(server['users'])+1,'name':new_name})
    users()

def users():
    print ('')
    print('=== Utilisateurs === \n')
    for user in server['users'] :
        print (user['id'],end='')
        print('.',user['name'])
    print('')
    print('o. Create user')
    print('x. Go back \n')
    choice2 = input('Select an option: ')
    if choice2 =='o' :
        new_name()
    elif choice2 =='x' :
        menu_principal()
    else:
        print('Unknown option:', choice2)
        users()

def new_channel() :
    new_channel = input('\nNew Chanel :')
    server['channels'].append({'id':len(server['channels'])+1,'name':new_channel, 'member_ids':[]})
    channels()

def channels():
    print ('')
    print('=== Channels === \n')
    ids={}
    for channel in server['channels'] :
        print (channel['id'],end='')
        print('.',channel['name'])
        ids[(str(channel['id']))]=None
    print('')
    print('o. Create channel')
    print('x. Go back \n')
    choice3 = input('Select an option: ')

    if choice3 in ids :
        show_messages(choice3)
    elif choice3 =='o' :
        new_channel()
    elif choice3 =='x' :
        menu_principal()
    else:
        print('Unknown option:', choice3)
        channels()
     
def show_messages(channel_id) :

    for channel in server['channels'] :
            if str(channel['id']) == str(channel_id) :
                break

    print('\n===',channel['name'],'===\n' )

    for message in server['messages'] :
        if str(message['channel']) == str(channel_id) :
            for user in server['users'] :
                if str(message['sender_id']) == str(user['id']) :
                    print('['+user['name']+']',end=' ')
            print(message['reception_date'])
            print('->',message['content'],'\n')
    print ('\ns. See members')
    print ('x. Go back\n')
    choice4 = input('Send a message : ')
    if choice4 == 's' :
        see_members(channel_id)
    elif choice4 == 'x' :
        channels()
    else : 
        send_message(channel_id, choice4)

def see_members(channel_id) :

    for channel in server['channels'] :
        if str(channel['id']) == str(channel_id) :
            break

    print('\n===',channel['name'],'members ===\n' )

    n=1
    for member_id in channel['member_ids'] :
        for user in server['users'] :
            if user['id'] == member_id :
                print(str(n)+'.',user['name'])
                n+=1

    

    print('\no. add member')
    print('x. Go back\n')

    choice4 = input('Select an option: ')
    if choice4 == 'o' :
        new_member(channel_id)
    elif choice4 =='x' :
        show_messages(channel_id)
    else : 
        print('Unknown option:', choice4)

def send_message(channel_id, message) :
    for user in server['users'] :
        if user['name'] == username : 
            sender_id = user['id']
    server['messages'].append({'id': len(server['messages'])+1, 'reception_date': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'sender_id': sender_id, 'channel': channel_id, 'content': message})
    show_messages(channel_id)

def new_member(channel_id) :
    new_member_name = input('\nNew member name :')
    members = {i['name'] : i['id'] for i in server['users']}
    if new_member_name in members :
        for channel in server['channels'] :
            if str(channel['id']) == str(channel_id) :
                channel['member_ids'].append(members[new_member_name])
        see_members(channel_id)
    else : 
        print('Unknown name:', new_member_name)
        see_members(channel_id)

def save(server_to_save : dict):
    json.dump(server_to_save, open(server_file_name,'w'))

print('\n=== Messenger ===\n')
identification()


#oscarceleplusbo



