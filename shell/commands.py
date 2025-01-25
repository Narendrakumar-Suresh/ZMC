import os
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)  # Automatically reset color after each print

def list_dir():
    arr = os.listdir()
    if len(arr) == 0:
        print(Fore.YELLOW + "Directory is empty")
    else:
        for i in arr:
            print(Fore.GREEN + f"--> {i}")

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def yell(command):
    if command.startswith("yell"):
        text = command[len("yell "):].strip()
        print(Fore.LIGHTMAGENTA_EX+text)

def chng_dir(command):
    if command.startswith("chdir"):
        path = command[len("chdir "):].strip()
        try:
            os.chdir(path)
            print(Fore.CYAN + f"Changed directory to: {os.getcwd()}")
        except FileNotFoundError:
            print(Fore.RED + f"Directory not found: {path}")
        except PermissionError:
            print(Fore.RED + f"Permission denied: {path}")

def back():
    """Navigate to the parent directory."""
    try:
        os.chdir("..")
        print(Fore.CYAN + f"Moved to Parent Directory: {os.getcwd()}")
    except Exception as e:
        print(Fore.RED + f"Error navigating to parent directory: {str(e)}")

def help():
    print(Fore.BLUE + """
Available commands:
    listdir            List all files and directories in the current directory
    cls                Clear the screen
    yell <text>        Print the text in uppercase
    chdir <path>       Change the current directory to the specified path
    back               Go to the parent directory
    exit               Exit the shell
    history            Show command history
    """)

def history(lis):
    if len(lis)!=0:
        for i in lis[::-1]:
            print(f'* {i}')
    else:
        print('Nothing here!')
