import os
import commands
import file_commands as fc
from colorama import Fore
from art import *
from termcolor import colored
import subprocess

text_art = text2art('Welcome to ZMC')
colored_art = colored(text_art,'cyan')
print(colored_art)
def main():
    hist=[]
    commands_map = {
        "listdir": commands.list_dir,
        "cls": commands.clear_screen,
        "help": commands.help,
        'back': commands.back,
        'history': lambda:commands.history(hist)
    }

    while True:
        prompt = Fore.WHITE + f"{os.getcwd()}" + Fore.YELLOW + "> "
        command = input(prompt).strip()
        if command == "exit":
            break
        elif command in commands_map:
            commands_map[command]()
        elif command.startswith("yell"):
            commands.yell(command)
        elif command.startswith("chdir"):
            commands.chng_dir(command)
        elif command.startswith("create"):
            fc.create(command)
        elif command.startswith("del"):
            fc.delete(command)
        elif command.startswith('mkdir'):
            fc.makedir(command)
        elif command.startswith('rndir'):
            fc.rename_dir(command)
        elif command.startswith('rmdir'):
            fc.delete_dir(command)
        else:
            try:
                subprocess.run(command, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                print(Fore.RED + f"Error: {e}")
            except FileNotFoundError:
                print(Fore.RED + "Command not found")

        hist.append(command)

if __name__ == "__main__":
    main()
