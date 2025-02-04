from datetime import datetime
import json
import os
import time
import sys

from user import User
from channel import Channel
from message import Message
from server import Server
from localserver import LocalServer
from remoteserver import RemoteServer

BOLD = "\033[1m"   # Texte en gras
GRAY = "\033[90m"  # Texte en gris clair
RED = "\033[91m"   # Texte en rouge
RESET = "\033[0m"  # Réinitialisation

class Client : 
    def __init__(self, server: LocalServer | RemoteServer ,  choice_identification : None | str = None, login : None | str = None, login_user : None | User = None, signin : None | str = None, choice_menu_principal : None | str = None, choice_users : None | str = None, choice_channels : None | str = None, choice_new_channel : None | str = None, choice_see_members : None | str = None, choice_new_member : None | str = None, unknown_identification : None | bool = None, unknown_login : None | bool = None, known_signin : None | bool = None, unknown_menu_principal : None | bool = None, unknown_users : None | bool = None, unknown_channels : None | bool = None, known_new_channel : None | bool = None, unknown_see_members : None | bool = None, known_new_member : None | bool = None, unknown_new_member : None | bool = None) :

        self.server = server
        self.login = login
        self.login_user = login_user
        self.signin = signin

        self.choice_identification = choice_identification
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
            LocalServer.save()
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
       
        dico_test = {user.name : user for user in self.server.get_users()}

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
        print(self.server.get_users())
        if self.signin in {user.name for user in self.server.get_users()} :
            self.known_signin = True
            self.sign_in()
        elif self.signin == 'x' :
            self.known_signin = False
            self.identification()
        else : 
            self.known_signin = False
            self.server.add_user(self.signin)
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
            LocalServer.save()
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
        for user in self.server.get_users() :
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

        for channel in self.server.get_channels() :
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
        ids={str(channel.id) : channel for channel in self.server.get_channels()}
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
        if self.choice_new_channel in {channel.name for channel in self.server.get_channels()} : 
            self.known_new_channel = True
            self.new_channel()
        elif self.choice_new_channel == 'x' :
            self.known_new_channel = False
            self.channels()
        else : 
            self.known_new_channel = False
            self.server.add_channel(self.choice_new_channel, self.login_user)
            self.channels()

    def show_messages(self, channel_id : str) :

        #mise en page
        self.clear_terminal()
        for channel in self.server.get_channels() :
                if str(channel.id) == str(channel_id) :
                    break
        print(f"{BOLD}=== {channel.name} ==={RESET}\n ")

        for message in self.server.get_messages(channel_id) :
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
            self.server.add_message(self.choice_show_messages,self.login_user,channel_id)
            self.show_messages(str(channel.id))

    def see_members(self, channel : Channel) :

        #mise en page
        self.clear_terminal()

        print(f'\n{BOLD}=== {channel.name} MEMEBRS ==={RESET}\n' )

        n=1
        for member_id in channel.member_ids :
            for user in self.server.get_users() :
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
            print(rf'{RED}/!\ Already registered member : {self.choice_new_members} {RESET}')
            self.choice_new_members = input( 'New member name: ')
        elif self.unknown_new_member == True :
            print(rf'{RED}/!\ Unknown username : {self.choice_new_members} {RESET}')
            self.choice_new_members = input( 'New member name: ')
        else :
            self.choice_new_members = input('\nNew member name: ')

        #réaction selon l'option choisie
        id_to_name = { user.id : user.name for user in self.server.get_users() }
        name_to_id = { user.name : user.id for user in self.server.get_users() }
        if self.choice_new_members in {id_to_name[id] for id in channel.member_ids}:
            self.known_new_member = True
            self.new_member(channel)
        elif self.choice_new_members not in name_to_id :
            self.unknown_new_member = True
            self.new_member(channel)
        else : 
            self.known_new_member = False
            self.unknown_new_member = False
            self.server.add_member(channel,name_to_id[self.choice_new_members])
            self.see_members(channel)

    @staticmethod

    def clear_terminal():
            # Efface le terminal en fonction du système d'exploitation
            os.system('cls' if os.name == 'nt' else 'clear')


