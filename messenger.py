from datetime import datetime

server = {
    'users': [
        {'id': 1, 'name': 'Alice'},
        {'id': 2, 'name': 'Bob'}
    ],
    'channels': [
        {'id': 1, 'name': 'Town square', 'member_ids': [1, 2]}
    ],
    'messages': [
        {
            'id': 1,
            'reception_date': datetime.now(),
            'sender_id': 1,
            'channel': 1,
            'content': 'Hi 👋'
        }
    ]
}




def menu_principal():
    print ('')
    print('=== Messenger === \n')
    print('1. See users')
    print('2. See channels \n')
    print('x. Leave \n')

    choice = input('Select an option: ')

    if choice == 'x':
        print('Bye! \n')
    elif choice == '1' :
        users()
    elif choice == '2' :
        channels()   
    else:
        print('Unknown option:', choice)

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

def new_channel() :
    new_channel = input('\nNew Chanel :')
    server['channels'].append({'id':len(server['channels'])+1,'name':new_channel})
    channels()

def channels():
    print ('')
    print('=== Channels === \n')
    for i in range(len(server['channels'])) :
        print (server['channels'][i]['id'],end='')
        print('.',server['channels'][i]['name'])
    print('')
    print('s. see channel members')
    print('o. Create channel')
    print('x. Go back \n')
    choice3 = input('Select an option: ')
    if choice3 =='s' :
        see_members()
    elif choice3 =='o' :
        new_channel()
    elif choice3 =='x' :
        menu_principal()
    else:
        print('Unknown option:', choice3)
     
def see_members() :
    channel_id = input('Select a channel : ')
    
    for i in range(len(server['channels'])) :
        channel = server['channels'][i]
        if channel['id'] == channel_id :
            break
    
    channel_members={}
    n=1
    for member_id in channel['member_ids'] :
        for i in range(len(server['users'])) :
            user = server['users'][i]
            if user['id'] == member_id :
                channel_members[n]=[user['id'],user['name']]
                n+=1
                
    print('===',channel['name'],'members ===\n' )
    print(user['id'], end ='')
    print('.',user['name'],'\n')


menu_principal()