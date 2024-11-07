from datetime import datetime
import json

with open('server-data.json','r') as fichier :
    server = json.load(fichier)


def menu_principal():
    print ('')
    print('=== Messenger === \n')
    print('1. See users')
    print('2. See channels \n')
    print('x. Save and exit \n')

    choice = input('Select an option: ')

    if choice == 'x':
        save()
        print('\nBye! \n')
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
    for i in range(len(server['users'])) :
        print (server['users'][i]['id'],end='')
        print('.',server['users'][i]['name'])
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
    for i in range(len(server['channels'])) :
        print (server['channels'][i]['id'],end='')
        print('.',server['channels'][i]['name'])
        ids[(str(server['channels'][i]['id']))]=''
    print('')
    print('o. Create channel')
    print('x. Go back \n')
    choice3 = input('Select an option: ')

    if choice3 in ids :
        see_members(choice3)
    elif choice3 =='o' :
        new_channel()
    elif choice3 =='x' :
        menu_principal()
    else:
        print('Unknown option:', choice3)
        channels()
     
def see_members(channel_id) :
    test ={ str(i+1) for i in range(len(server['channels']))}
    print(test)

    if channel_id in test :
        for channel in server['channels'] :
            if str(channel['id']) == str(channel_id) :
                break
        print(channel)

        print('\n===',channel['name'],'members ===\n' )
        n=1

        for member_id in channel['member_ids'] :
            for user in server['users'] :
                if user['id'] == member_id :
                    print(n,end='')
                    print('.',user['name'])
                    n+=1

        

        print('\no. add member')
        print('x. back\n')

        choice4 = input('Select an option: ')
        if choice4 == 'o' :
            new_member(channel_id)
        elif choice4 =='x' :
            channels()
        else : 
            print('Unknown option:', choice4)
    
    else:
        print('Unknown option:', channel_id)


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

def save():
    with open('server-data.json','w') as fichier :
        json.dump(server, fichier, indent=4, ensure_ascii=False)


menu_principal()