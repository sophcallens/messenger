import time
import argparse
import sys

from server import Server
from client import Client

#On veut mettre "server-data.json" dans server_file_name sachant qu'il est en paramètre
parser = argparse.ArgumentParser()
parser.add_argument('--filename','-f', help='enter json path')
parser.add_argument('--url','-u', help='enter url')
args = parser.parse_args()

#definition du serveur
server : Server

if args.filename is not None : 
    server = Server.filename_to_server(args.filename)
elif args.url is not None : 
    server = Server.url_to_server(args.url)
else :
    print('TypeError: Pas de server selectionné')
    sys.exit(1)
    
Client.clear_terminal()
print ('\nLe server ouvert est : ', server.file_name)
time.sleep(1)

client = Client(server)

#début du programme
client.clear_terminal()
client.identification()




