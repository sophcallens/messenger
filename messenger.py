from datetime import datetime
import json
import os
import time
import argparse
import sys


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

choice_identification = None
login = None
login_user = None
signin = None
choice_menu_principal = None
choice_users = None
choice_channels = None
choice_new_channel = None
choice_see_members = None
choice_new_member = None

unknown_identification = False
unknown_login = False
known_signin = False
unknown_menu_principal = False
unknown_users = False
unknown_channels = False
known_new_channel = False
unknown_see_members = False
known_new_member = False
unknown_new_member = False

def identification() :

    #mise en page
    clear_terminal()
    print(f'\n{BOLD}=== Messenger ==={RESET}\n')
    print('1. log in')
    print('2. sign in\n' )
    print(f'{GRAY}x. Exit{RESET} \n')

    #possibilité d'un message d'erreur
    global unknown_identification
    global choice_identification

    if unknown_identification == True : 
        print(rf'{RED}/!\ Unknown option : {choice_users} {RESET}')
        choice_identification = input('Select an option: ')
    else :
        choice_identification = input('\nSelect an option: ')

    #réaction selon l'option choisie 
    if choice_identification =='1' :
        unknown_identification = False
        log_in()
    elif choice_identification =='2' :
        unknown_identification = False
        sign_in()
    elif choice_identification =='x' :
        save(server)
        print('\n-> Bye! \n')
        time.sleep(1)
        clear_terminal()
    else:
        unknown_identification = True
        identification()

def log_in(): 

    #mise en page
    clear_terminal()
    print(f'\n{BOLD}=== Log in ==={RESET}\n')
    print(f'{GRAY}x. Exit{RESET} \n')

    #possibilité d'un message d'erreur
    global unknown_login  
    global login 
    global login_user

    if unknown_login == True : 
        print(rf'{RED}/!\ Unknown username : {login} {RESET}')
        login = input( 'username : ')
    else :
        login = input('\nusername : ')

    #réaction selon l'option choisie 
    dico_test = {user.name : user for user in server.users}
    if login in dico_test :
        login_user = dico_test[login] #on en aura besoin dans la fonction channels et new_member
        unknown_login = False
        print('\n-> Welcome',login,'!')
        time.sleep(1)
        menu_principal()
    elif login == 'x' :
        unknown_login = False
        identification()
    else : 
        unknown_login = True
        log_in()

def sign_in() :

    #mise en page
    clear_terminal()
    print(f'\n{BOLD}=== Sign in ==={RESET}\n')
    print(f'{GRAY}x. Exit{RESET} \n')

    #possibilité d'un message d'erreur
    global known_signin  
    global signin 

    if known_signin == True : 
        print(rf'{RED}/!\ Already existing username : {signin} {RESET}')
        signin = input( 'Your name : ')
    else :
        signin = input('\nYour name : ')

    #réaction selon l'option choisie 
    if signin in {user.name for user in server.users} :
        known_signin = True
        sign_in()
    elif signin == 'x' :
        known_signin = False
        identification()
    else : 
        known_signin = False
        server.users.append(User(len(server.users)+1, signin))
        identification()

    #réaction selon l'option choisie 
    if signin == 'x' :
        identification()
    else :
        server.users.append(User(len(server.users)+1, signin))
        identification()

def menu_principal():
    
    #mise en page
    clear_terminal()
    print(f"\n{BOLD}=== Menu principal === {RESET}\n ")
    print('1. See users')
    print('2. See channels \n')
    print(f'{GRAY}x. Save and Exit{RESET} \n')

    #possibilité d'un message d'erreur
    global unknown_menu_principal
    global choice_menu_principal

    if unknown_menu_principal == True : 
        print(rf'{RED}/!\ Unknown option : {choice_menu_principal} {RESET}')
        choice_menu_principal = input('Select an option: ')
    else :
        choice_menu_principal = input('\nSelect an option: ')

    #réaction selon l'option choisie 
    if choice_menu_principal == 'x':
        unknown_menu_principal = False
        save(server)
        print('\n-> Bye! \n')
        time.sleep(1)
        clear_terminal()
    elif choice_menu_principal == '1' :
        unknown_menu_principal = False
        users()
    elif choice_menu_principal == '2' :
        unknown_menu_principal = False
        channels()   
    else:
        unknown_menu_principal = True
        menu_principal()

def users():

    #mise en page
    clear_terminal()
    print(f'\n{BOLD}=== Utilisateurs ==={RESET} \n')
    for user in server.users :
        print (f'{user.id}.{user.name}')
    print(f'\n{GRAY}x. Go back {RESET}\n')

    #possibilité de message d'erreur
    global unknown_users
    global choice_users

    if unknown_users == True : 
        print(rf'{RED}/!\ Unknown option : {choice_users} {RESET}')
        choice_users = input('Select an option: ')
    else :
        choice_users = input('\nSelect an option: ')

    #réaction selon l'option choisie
    if choice_users =='x' :
        unknown_users = False
        menu_principal()
    else:
        unknown_users = True
        users()

def channels():

    #mise en page
    clear_terminal()
    print(f'\n{BOLD}=== Channels ==={RESET} \n')

    for channel in server.channels :
        if login_user.id in channel.member_ids : 
            print (channel.id,end='')
            print('.',channel.name)
    print(f'\n{GRAY}o. Create channel{RESET}')
    print(f'{GRAY}x. Go back {RESET}\n')

    #possibilité d'un message d'erreur
    global unknown_channels
    global choice_channels

    if unknown_channels == True : 
        print(rf'{RED}/!\ Unknown option : {choice_channels} {RESET}')
        choice_channels = input('Select an option: ')
    else :
        choice_channels = input('\nSelect an option: ')

    #réaction selon l'option choisie
    ids={str(channel.id) : channel for channel in server.channels}
    if choice_channels in ids and login_user.id in ids[choice_channels].member_ids :
        unknown_channels = False
        show_messages(choice_channels)
    elif choice_channels =='o' :
        unknown_channels = False
        new_channel()
    elif choice_channels =='x' :
        unknown_channels = False
        menu_principal()
    else:
        unknown_channels = True
        channels()
     
def new_channel() :

    #mise en page
    clear_terminal()
    print(f'\n{BOLD}=== New channel ==={RESET} \n')

    #possibilité d'un message d'erreur
    global known_new_channel 
    global choice_new_channel

    if known_new_channel == True : 
        print(rf'{RED}/!\ Already existing channel : {choice_new_channel} {RESET}')
        choice_new_channel = input('Select an option: ')
    else :
        choice_new_channel = input('\nSelect an option: ')

    #réaction selon l'option choisie
    if choice_new_channel in {channel.name for channel in server.channels} : 
        known_new_channel = False
        server.channels.append(Channel(len(server.channels)+1, new_channel, [login_user.id]))
        channels()
    else : 
        known_new_channel = True
        new_channel()

def show_messages(channel_id : str) :

    #mise en page
    clear_terminal()
    for channel in server.channels :
            if str(channel.id) == str(channel_id) :
                break
    print(f"{BOLD}=== {channel.name} ==={RESET}\n ")

    for message in server.messages :
        if str(message.channel) == str(channel.id) :
            for user in server.users :
                if str(message.sender_id) == str(user.id) :
                    print('[' + user.name + ']',end=' ')
            print(f"{GRAY}{message.reception_date}{RESET}")
            print('->',message.content,'\n')
    print (f'\n{GRAY}s. See members')
    print (f'x. Go back{RESET}\n')

    #envoyer un message ou choisir une option
    choice_show_messages = input( 'Send a message : ')

    if choice_show_messages == 's' :
        see_members(channel)
    elif choice_show_messages == 'x' :
        channels()
    else : #envoie d'un message
        server.messages.append(Message(len(server.messages)+1, datetime.now().strftime("%d/%m/%Y %H:%M:%S"), login_user.id, channel_id, choice_show_messages))
        show_messages(str(channel.id))

def see_members(channel : Channel) :

    #mise en page
    clear_terminal()

    print(f'\n{BOLD}=== {channel.name} members ==={RESET}\n' )

    n=1
    for member_id in channel.member_ids :
        for user in server.users :
            if user.id == member_id :
                print(str(n)+'.',user.name)
                n+=1

    print(f'\n{GRAY}o. add member')
    print(f'x. Go back{RESET}\n')

    #possibilité d'un message d'erreur
    global unknown_see_members
    global choice_see_members

    if unknown_see_members == True : 
        print(rf'{RED}/!\ Unknown option : {choice_see_members} {RESET}')
        choice_see_members = input( 'Select an option: : ')
    else :
        choice_see_members = input('\nSelect an option: : ')

    #réaction selon l'option choisie
    if choice_see_members == 'o' :
        unknown_see_members = False
        new_member(channel)
    elif choice_see_members =='x' :
        unknown_see_members = False
        show_messages(str(channel.id))
    else : 
        unknown_see_members = True
        see_members(channel)

def new_member(channel : Channel) :

    #mise en page
    clear_terminal()
    print(f'\n{BOLD}=== New {channel.name} member ==={RESET}\n' )

    #possibilité d'un message d'erreur
    global known_new_member
    global unknown_new_member
    global choice_new_members

    if known_new_member == True : 
        print(rf'{RED}/!\ Already registered memebr : {choice_new_members} {RESET}')
        choice_new_members = input( 'New member name: ')
    elif unknown_new_member == True :
        print(rf'{RED}/!\ Unknown username : {choice_new_members} {RESET}')
        choice_new_members = input( 'New member name: ')
    else :
        choice_new_members = input('\nNew member name: ')

    #réaction selon l'option choisie
    id_to_name = { user.id : user.name for user in server.users }
    name_to_id = { user.name : user.id for user in server.users }
    if choice_new_members in {id_to_name[id] for id in channel.member_ids}:
        known_new_member = True
        new_member(channel)
    elif choice_new_members not in name_to_id :
        unknown_new_member = True
        new_member(channel)
    else : 
        known_new_member = False
        unknown_new_member = False
        channel.member_ids.append(name_to_id[choice_new_members])
        see_members(channel)

def save(server_to_save : Server):
    new_server = {}
    new_server['users']= [user.to_dict() for user in server_to_save.users] 
    new_server['channels']=[channel.to_dict() for channel in server_to_save.channels] 
    new_server['messages'] = [message.to_dict() for message in server_to_save.messages]
    
    with open(server_file_name,'w') as json_file :
        json.dump(new_server,json_file)

def clear_terminal():
    # Efface le terminal en fonction du système d'exploitation
    os.system('cls' if os.name == 'nt' else 'clear')



#On veut mettre "server-data.json" dans server_file_name sachant qu'il est en paramètre
parser = argparse.ArgumentParser()
parser.add_argument('--server','-s', help='enter json path')
args = parser.parse_args()
server_file_name = args.server

#affichage d'un message d'erreur si le sever n'est pas renseigné
if server_file_name == None :
    print('TypeError: Pas de server selectionné, correction proposée : \npython messenger.py -s <server path>')
    sys.exit(1)
else : 
    clear_terminal()
    print ('\nLe server ouvert est : ', server_file_name)
    time.sleep(1)

#overture du server
with open(server_file_name) as json_file :
    server_dict = json.load(json_file)

server = Server.from_dict(server_dict)

#début du programme
clear_terminal()
identification()




