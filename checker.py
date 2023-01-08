import json
import os
import random
import colorama
import web3
from web3 import Web3, HTTPProvider


with open("settings.json", "r") as settings_file:
    settings = json.load(settings_file)['settings'][0]

node = settings['node']
contract_address = settings['contract']
abi = settings['abi']
get_file = settings['get_domains']
write_file = settings['write_domains']
function = settings['function']



w3 = web3.Web3(web3.HTTPProvider(node))
web3 = Web3(HTTPProvider(node))


contract = web3.eth.contract(address=contract_address, abi=abi)


def string_to_bytes32_hex(string):
  string_bytes = string.encode("utf-8")
  padded_bytes = string_bytes.ljust(32, b"\0")
  return w3.toHex(padded_bytes)


def clear():
  os.system('cls')


def check_random_domains():
  checked = 0

  length = int(input(f'Input the lenght of the domain name >>> '))

  clear()

  print('Select the character set:')
  print('[1] 0123456789')
  print('[2] abcdefghijklmnopqrstuvwxyz')
  print('[3] 0123456789abcdefghijklmnopqrstuvwxyz')
  print('[4] CUSTOM')
  print()

  select_character_set_option = int(input('Enter your option >>> '))

  clear()

  if select_character_set_option == 1:
    charset = "1","2","3","4","5","6","7","8","9","0"
  elif select_character_set_option == 2:
    charset = "a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"
  elif select_character_set_option == 3:
    charset = "1","2","3","4","5","6","7","8","9","0","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"
  elif select_character_set_option == 4:
    print('You can use numbers from 0 to 9 and lowercase letters. Use the following syntax: 123abc')
    print()
    charset = input('Custom character set >>> ')

  clear()

  number = int(input('How many domain names should be checked? >>> '))

  clear()

  for i in range(number):

    random_string = ''.join(random.choice(charset) for i in range(int(length)))

    all_names = open(write_file, 'r').read()

    bytes32_hex = string_to_bytes32_hex(random_string)

    result = contract.functions[function](bytes32_hex).call()
    
    if result == '0x0000000000000000000000000000000000000000' and all_names.find(random_string) == -1:

      with open(write_file, 'a') as f:
        f.writelines(f'{random_string}\n')

      color = colorama.Fore.GREEN

    else:

      color = colorama.Fore.RED

    checked = checked + 1

    print('Checked', color + colorama.Style.BRIGHT + str(checked) + colorama.Style.RESET_ALL, 'domain names!', end='\r')

  input('\ndone')


def check_file():

  checked = 0

  file = open(get_file,'r').read().splitlines()

  clear()

  for line in file:
    
    string = line

    bytes32_hex = string_to_bytes32_hex(string)

    result = contract.functions[function](bytes32_hex).call()
    
    if result == '0x0000000000000000000000000000000000000000':

      with open((write_file), 'a') as f:
        f.writelines(f'{string}\n')

      color = colorama.Fore.GREEN

    else:

      color = colorama.Fore.RED

    checked = checked + 1

    print('Checked', color + colorama.Style.BRIGHT + str(checked) + colorama.Style.RESET_ALL, 'domain names!', end='\r')

  input('\ndone')


clear()

print('[1] Check domain names based on random strings with a specific length and character set.')
print('[2] Check domain names given in a specific text file.')
print('Note: In both cases, the available domain names are saved in a file called "available.txt".')
print()

option = int(input('Enter your option >>> '))

if option == 1:
  clear()
  check_random_domains()
elif option == 2:
  clear()
  check_file()