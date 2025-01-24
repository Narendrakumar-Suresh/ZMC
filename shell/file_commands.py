from colorama import Fore, Style
import os
def create(cmd):
    file_name=cmd[7:].strip()
    try:
        with open(file_name,"x"):
            print(Fore.GREEN +f'Successfully created {file_name}')
    except FileExistsError:
        print(Fore.YELLOW ++f'{file_name} already exists!!')
    except Exception as e:
        print(Fore.RED+f'Cannot create file {e}')

def delete(cmd):
    file_name=cmd[4:].strip()
    try:
        os.remove(file_name)
        print(Fore.GREEN +f'Successfully deleted {file_name}')
    except FileNotFoundError:
        print(Fore.RED +f'{file_name} not found!')
    except Exception as e:
        print(Fore.RED+f'Cannot create file {e}')

