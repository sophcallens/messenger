from datetime import datetime
import json
import os
import time

BOLD = "\033[1m"   # Texte en gras
GRAY = "\033[90m"  # Texte en gris clair
RED = "\033[91m"   # Texte en rouge
RESET = "\033[0m"  # Réinitialisation


class User:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
    @classmethod
    def from_dict(cls, user_dict: dict) -> 'User': 
        return cls(user_dict['id'],user_dict['name'])

    def to_dict(self) :
        return {'id': self.id, 'name': self.name }

class Channel:
    def __init__(self, id: int, name: str, member_ids: list):
        self.id = id
        self.name = name
        self.member_ids = member_ids
    @classmethod
    def from_dict(cls, channel_dict: dict) -> 'Channel': 
        return cls(channel_dict['id'],channel_dict['name'],channel_dict['member_ids'])

    def to_dict(self) :
        return {'id':self.id, 'name':self.name, 'member_ids': self.member_ids}

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

class Server :
    def __init__(self,users : list['User'],channels: list['Channel'], messages: list['Message']) :
        self.users = users
        self.channels = channels
        self.messages = messages
    
    @classmethod
    def from_dict(cls,server_dict : dict) -> 'Server' :

        new_server = Server([],[],[])
        for user in server_dict['users'] :
            new_server.users.append(User.from_dict(user))
        for channel in server_dict['channels'] : 
            new_server.channels.append(Channel.from_dict(channel))
        for message in server_dict['messages'] : 
            new_server.messages.append(Message.from_dict(message))
        return new_server


server_file_name = 'server-data.json'
with open(server_file_name) as json_file :
    server_dict = json.load(json_file)

server = Server.from_dict(server_dict)

username = None
unknown = False

def identification() :
    print(f'\n{BOLD}=== Messenger ==={RESET}\n')
    global username 
    global unknown
    print(f'{GRAY}x. Exit{RESET} \n')
    if unknown == True : 
            print(f'{RED}/!\ Unknown username : {username} {RESET}')
            username = input( 'username : ')
    if unknown == False :
        username = input('\nusername : ')

    if username in {user.name for user in server.users} :
        print('\n-> Welcome',username,'!')
        time.sleep(1)
        menu_principal()
    elif username == 'x' :
        save(server)
        print('\n-> Bye! \n')
    else : 
        unknown = True
        clear_terminal()
        identification()

def menu_principal():

    clear_terminal()
    print ('')
    print(f"{BOLD}=== Menu principal === {RESET}\n ")
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
    clear_terminal()
    new_name = input('\nNew Name :')
    server.users.append(User(len(server.users)+1, new_name))
    users()

def users():
    clear_terminal()
    print ('')
    print(f'{BOLD}=== Utilisateurs ==={RESET} \n')
    for user in server.users :
        print (user.id,end='')
        print('.',user.name)
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
    clear_terminal()
    new_channel = input('\nNew Chanel :')
    clear_terminal()
    server.channels.append(Channel(len(server.channels)+1, new_channel, []))
    channels()

def channels():
    clear_terminal()
    print ('')
    print(f'{BOLD}=== Channels ==={RESET} \n')
    for channel in server.channels :
        print (channel.id,end='')
        print('.',channel.name)
    print('')
    print('o. Create channel')
    print('x. Go back \n')
    choice3 = input('Select an option: ')

    ids={str(channel.id) for channel in server.channels}
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
    clear_terminal()

    for channel in server.channels :
            if str(channel.id) == str(channel_id) :
                break

    print(f"{BOLD}=== {channel.name} ==={RESET}\n ")

    for message in server.messages :
        if str(message.channel) == str(channel_id) :
            for user in server.users :
                if str(message.sender_id) == str(user.id) :
                    print('[' + user.name + ']',end=' ')
            print(f"{GRAY}{message.reception_date}{RESET}")
            print('->',message.content,'\n')
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
    clear_terminal()

    for channel in server.channels :
        if str(channel.id) == str(channel_id) :
            break

    print(f'\n{BOLD}=== {channel.name} members ==={RESET}\n' )

    n=1
    for member_id in channel.member_ids :
        for user in server.users :
            if user.id == member_id :
                print(str(n)+'.',user.name)
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
    clear_terminal()

    for user in server.users :
        if user.name == username : 
            sender_id = user.id
    server.messages.append(Message(len(server.messages)+1, datetime.now().strftime("%d/%m/%Y %H:%M:%S"), sender_id, channel_id, message))
    show_messages(channel_id)

def new_member(channel_id) :
    clear_terminal()

    new_member_name = input('\nNew member name :')
    clear_terminal()
    members = {user.name : user.id for user in server.users}
    if new_member_name in members :
        for channel in server.channels :
            if str(channel.id) == str(channel_id) :
                channel.member_ids.append(members[new_member_name])
        see_members(channel_id)
    else : 
        print('Unknown name:', new_member_name)
        see_members(channel_id)

def save(server_to_save : Server):
    clear_terminal()
    new_server = {}
    new_server['users']= [user.to_dict() for user in server_to_save.users] 
    new_server['channels']=[channel.to_dict() for channel in server_to_save.channels] 
    new_server['messages'] = [message.to_dict() for message in server_to_save.messages]
    
    with open(server_file_name,'w') as json_file :
        json.dump(new_server,json_file)

def clear_terminal():
    # Efface le terminal en fonction du système d'exploitation
    os.system('cls' if os.name == 'nt' else 'clear')

clear_terminal()
identification()


#oscarceleplusbo



