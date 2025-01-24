import os
import commands
import file_commands as fc
from colorama import Fore, Style
from art import *
from termcolor import colored

text_art = text2art('Welcome to Neoshell')
colored_art = colored(text_art, 'green')
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
        else:
            print(Fore.RED + "Invalid command")
        hist.append(command)

if __name__ == "__main__":
    main()
