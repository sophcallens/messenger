import sys

print(sys.argv)

commit_message=''
#On veut mettre "mon message de commit" dansc commit_message

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-m', '--message')

args = parser.parse_args()

print('ArgumentParser a parsé le paramètre suivant : ', args.message)
commit_message = args.message