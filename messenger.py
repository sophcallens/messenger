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
    def __init__(self,file_name : str, users : list['User'],channels: list['Channel'], messages: list['Message']) :
        self.file_name = file_name
        self.users = users
        self.channels = channels
        self.messages = messages
    
    @classmethod
    def from_dict(cls,file_name,server_dict : dict) -> 'Server' :

        new_server = Server(file_name,[],[],[])
        for user in server_dict['users'] :
            new_server.users.append(User.from_dict(user))
        for channel in server_dict['channels'] : 
            new_server.channels.append(Channel.from_dict(channel))
        for message in server_dict['messages'] : 
            new_server.messages.append(Message.from_dict(message))
        return new_server

class Client : 
    def __init__(self, server: Server,  choice_identification : None | str = None, login : None | str = None, login_user : None | User = None, signin : None | str = None, choice_menu_principal : None | str = None, choice_users : None | str = None, choice_channels : None | str = None, choice_new_channel : None | str = None, choice_see_members : None | str = None, choice_new_member : None | str = None, unknown_identification : None | bool = None, unknown_login : None | bool = None, known_signin : None | bool = None, unknown_menu_principal : None | bool = None, unknown_users : None | bool = None, unknown_channels : None | bool = None, known_new_channel : None | bool = None, unknown_see_members : None | bool = None, known_new_member : None | bool = None, unknown_new_member : None | bool = None) :

        self.server = server
        self.choice_identification = choice_identification
        self.login = login
        self.login_user = login_user
        self.signin = signin
        self.choice_menu_principal = choice_menu_principal
        self.choice_users = choice_users
        self.choice_channels = choice_channels
        self.choice_new_channel = choice_new_channel
        self.choice_see_members = choice_see_members
        self.choice_new_member = choice_new_member

        self.unknown_identification = unknown_identification
        self.unknown_login = unknown_login
        self.known_signin = known_signin
        self.unknown_menu_principal = unknown_menu_principal
        self.unknown_users = unknown_users
        self.unknown_channels = unknown_channels
        self.known_new_channel = known_new_channel
        self.unknown_see_members = unknown_see_members
        self.known_new_member = known_new_member
        self.unknown_new_member = unknown_new_member

    

    def identification(self) :

        #mise en page
        self.clear_terminal()
        print(f'\n{BOLD}=== MESSENGER ==={RESET}\n')
        print('1. log in')
        print('2. sign in\n' )
        print(f'{GRAY}x. Close Messenger{RESET} \n')

        #possibilité d'un message d'erreur
        if self.unknown_identification == True : 
            print(rf'{RED}/!\ Unknown option : {self.choice_identification} {RESET}')
            self.choice_identification = input('Select an option: ')
        else :
            self.choice_identification = input('\nSelect an option: ')

        #réaction selon l'option choisie 
        if self.choice_identification =='1' :
            self.unknown_identification = False
            self.log_in()
        elif self.choice_identification =='2' :
            self.unknown_identification = False
            self.sign_in()
        elif self.choice_identification =='x' :
            self.save()
            print('\n-> Closing messenegr ... \n')
            time.sleep(1)
            self.clear_terminal()
            sys.exit(0)
        else:
            self.unknown_identification = True
            self.identification()

    def log_in(self): 

        #mise en page
        self.clear_terminal()
        print(f'\n{BOLD}=== LOG IN ==={RESET}\n')
        print(f'{GRAY}x. Go back{RESET} \n')

        #possibilité d'un message d'erreur
        if self.unknown_login == True : 
            print(rf'{RED}/!\ Unknown username : {self.login} {RESET}')
            self.login = input( 'username : ')
        else :
            self.login = input('\nusername : ')

        #réaction selon l'option choisie 
        dico_test = {user.name : user for user in self.server.users}
        if self.login in dico_test :
            self.login_user = dico_test[self.login] #on en aura besoin dans la fonction channels et new_member
            self.unknown_login = False
            print('\n-> Welcome',self.login,'!')
            time.sleep(1)
            self.menu_principal()
        elif self.login == 'x' :
            self.unknown_login = False
            self.identification()
        else : 
            self.unknown_login = True
            self.log_in()

    def sign_in(self) :

        #mise en page
        self.clear_terminal()
        print(f'\n{BOLD}=== SIGN IN ==={RESET}\n')
        print(f'{GRAY}x. Go back{RESET} \n')

        #possibilité d'un message d'erreur
        if self.known_signin == True : 
            print(rf'{RED}/!\ Already existing username : {self.signin} {RESET}')
            self.signin = input( 'Your name : ')
        else :
            self.signin = input('\nYour name : ')

        #réaction selon l'option choisie 
        if self.signin in {user.name for user in self.server.users} :
            self.known_signin = True
            self.sign_in()
        elif self.signin == 'x' :
            self.known_signin = False
            self.identification()
        else : 
            self.known_signin = False
            self.server.users.append(User(len(self.server.users)+1, self.signin))
            self.identification()

        #réaction selon l'option choisie 
        if self.signin == 'x' :
            self.identification()
        else :
            self.server.users.append(User(len(self.server.users)+1, self.signin))
            self.identification()

    def menu_principal(self):
        
        #mise en page
        self.clear_terminal()
        print(f"\n{BOLD}=== MAIN MENU === {RESET}\n ")
        print('1. See users')
        print('2. See channels \n')
        print(f'\n{GRAY}x. log out{RESET} \n')

        #possibilité d'un message d'erreur
        if self.unknown_menu_principal == True : 
            print(rf'{RED}/!\ Unknown option : {self.choice_menu_principal} {RESET}')
            self.choice_menu_principal = input('Select an option: ')
        else :
            self.choice_menu_principal = input('\nSelect an option: ')

        #réaction selon l'option choisie 
        if self.choice_menu_principal == 'x':
            self.unknown_menu_principal = False
            self.save()
            print(f'\n-> Bye {self.login}! \n')
            time.sleep(1)
            self.identification()
        elif self.choice_menu_principal == '1' :
            self.unknown_menu_principal = False
            self.users()
        elif self.choice_menu_principal == '2' :
            self.unknown_menu_principal = False
            self.channels()   
        else:
            self.unknown_menu_principal = True
            self.menu_principal()

    def users(self):

        #mise en page
        self.clear_terminal()
        print(f'\n{BOLD}=== USERS ==={RESET} \n')
        for user in self.server.users :
            print (f'{user.id}.{user.name}')
        print(f'\n\n{GRAY}x. Go back {RESET}\n')

        #possibilité de message d'erreur
        if self.unknown_users == True : 
            print(rf'{RED}/!\ Unknown option : {self.choice_users} {RESET}')
            self.choice_users = input('Select an option: ')
        else :
            self.choice_users = input('\nSelect an option: ')

        #réaction selon l'option choisie
        if self.choice_users =='x' :
            self.unknown_users = False
            self.menu_principal()
        else:
            self.unknown_users = True
            self.users()

    def channels(self):

        #mise en page
        self.clear_terminal()
        print(f'\n{BOLD}=== CHANNELS ==={RESET} \n')

        for channel in self.server.channels :
            if self.login_user.id in channel.member_ids : 
                print (f'{channel.id}. {channel.name}')
        print(f'\n\n{GRAY}o. Create channel{RESET}')
        print(f'{GRAY}x. Go back {RESET}\n')

        #possibilité d'un message d'erreur
        if self.unknown_channels == True : 
            print(rf'{RED}/!\ Unknown option : {self.choice_channels} {RESET}')
            self.choice_channels = input('Select an option: ')
        else :
            self.choice_channels = input('\nSelect an option: ')

        #réaction selon l'option choisie
        ids={str(channel.id) : channel for channel in self.server.channels}
        if self.choice_channels in ids and self.login_user.id in ids[self.choice_channels].member_ids :
            self.unknown_channels = False
            self.show_messages(self.choice_channels)
        elif self.choice_channels =='o' :
            self.unknown_channels = False
            self.new_channel()
        elif self.choice_channels =='x' :
            self.unknown_channels = False
            self.menu_principal()
        else:
            self.unknown_channels = True
            self.channels()
        
    def new_channel(self) :

        #mise en page
        self.clear_terminal()
        print(f'\n{BOLD}=== NEW CHANNEL ==={RESET} \n')
        print(f'{GRAY}x. Go back{RESET}\n')

        #possibilité d'un message d'erreur
        if self.known_new_channel == True : 
            print(rf'{RED}/!\ Already existing channel : {self.choice_new_channel} {RESET}')
            self.choice_new_channel = input('New channel name: ')
        else :
            self.choice_new_channel = input('\nNew channel name: ')

        #réaction selon l'option choisie
        if self.choice_new_channel in {channel.name for channel in self.server.channels} : 
            self.known_new_channel = True
            self.new_channel()
        elif self.choice_new_channel == 'x' :
            self.known_new_channel = False
            self.channels()
        else : 
            self.known_new_channel = False
            self.server.channels.append(Channel(len(self.server.channels)+1, self.choice_new_channel, [self.login_user.id]))
            self.channels()

    def show_messages(self, channel_id : str) :

        #mise en page
        self.clear_terminal()
        for channel in self.server.channels :
                if str(channel.id) == str(channel_id) :
                    break
        print(f"{BOLD}=== {channel.name} ==={RESET}\n ")

        for message in self.server.messages :
            if str(message.channel) == str(channel.id) :
                for user in self.server.users :
                    if str(message.sender_id) == str(user.id) :
                        print('[' + user.name + ']',end=' ')
                print(f"{GRAY}{message.reception_date}{RESET}")
                print('->',message.content,'\n')
        print (f'\n{GRAY}s. See members')
        print (f'x. Go back{RESET}\n')

        #envoyer un message ou choisir une option
        self.choice_show_messages = input( 'Send a message : ')

        if self.choice_show_messages == 's' :
            self.see_members(channel)
        elif self.choice_show_messages == 'x' :
            self.channels()
        else : #envoie d'un message
            self.server.messages.append(Message(len(self.server.messages)+1, datetime.now().strftime("%d/%m/%Y %H:%M:%S"), self.login_user.id, channel_id, self.choice_show_messages))
            self.show_messages(str(channel.id))

    def see_members(self, channel : Channel) :

        #mise en page
        self.clear_terminal()

        print(f'\n{BOLD}=== {channel.name} MEMEBRS ==={RESET}\n' )

        n=1
        for member_id in channel.member_ids :
            for user in self.server.users :
                if user.id == member_id :
                    print(str(n)+'.',user.name)
                    n+=1

        print(f'\n{GRAY}o. add member')
        print(f'x. Go back{RESET}\n')

        #possibilité d'un message d'erreur
        if self.unknown_see_members == True : 
            print(rf'{RED}/!\ Unknown option : {self.choice_see_members} {RESET}')
            self.choice_see_members = input( 'Select an option: : ')
        else :
            self.choice_see_members = input('\nSelect an option: : ')

        #réaction selon l'option choisie
        if self.choice_see_members == 'o' :
            self.unknown_see_members = False
            self.new_member(channel)
        elif self.choice_see_members =='x' :
            self.unknown_see_members = False
            self.show_messages(str(channel.id))
        else : 
            self.unknown_see_members = True
            self.see_members(channel)

    def new_member(self, channel : Channel) :

        #mise en page
        self.clear_terminal()
        print(f'\n{BOLD}=== NEW {channel.name} MEMEBR ==={RESET}\n' )

        #possibilité d'un message d'erreur
        if self.known_new_member == True : 
            print(rf'{RED}/!\ Already registered memebr : {self.choice_new_members} {RESET}')
            self.choice_new_members = input( 'New member name: ')
        elif self.unknown_new_member == True :
            print(rf'{RED}/!\ Unknown username : {self.choice_new_members} {RESET}')
            self.choice_new_members = input( 'New member name: ')
        else :
            self.choice_new_members = input('\nNew member name: ')

        #réaction selon l'option choisie
        id_to_name = { user.id : user.name for user in self.server.users }
        name_to_id = { user.name : user.id for user in self.server.users }
        if self.choice_new_members in {id_to_name[id] for id in channel.member_ids}:
            self.known_new_member = True
            self.new_member(channel)
        elif self.choice_new_members not in name_to_id :
            self.unknown_new_member = True
            self.new_member(channel)
        else : 
            self.known_new_member = False
            self.unknown_new_member = False
            channel.member_ids.append(name_to_id[self.choice_new_members])
            self.see_members(channel)

    def save(self):
            new_server = {
            'users': [user.to_dict() for user in self.server.users],
            'channels': [channel.to_dict() for channel in self.server.channels],
            'messages': [message.to_dict() for message in self.server.messages],
            }

            with open(self.server.file_name, 'w') as json_file:
                json.dump(new_server, json_file)

    @staticmethod

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
    print('TypeError: Pas de server selectionné, correction proposée : python messenger.py -s <server path>')
    sys.exit(1)
else : 
    Client.clear_terminal()
    print ('\nLe server ouvert est : ', server_file_name)
    time.sleep(1)

#overture du server
with open(server_file_name) as json_file :
    server_dict = json.load(json_file)

client = Client(Server.from_dict(server_file_name, server_dict))


#début du programme
client.clear_terminal()
client.identification()




