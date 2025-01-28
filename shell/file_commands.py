from colorama import Fore, Style
import os

'''
This has commands related to files
'''
# create file
def create(cmd):
    file_name=cmd[7:].strip()
    try:
        with open(file_name,"x"):
            print(Fore.GREEN +f'Successfully created {file_name}')
    except FileExistsError:
        print(Fore.YELLOW ++f'{file_name} already exists!!')
    except Exception as e:
        print(Fore.RED+f'Cannot create file {e}')

# delete file
def delete(cmd):
    file_name=cmd[4:].strip()
    try:
        os.remove(file_name)
        print(Fore.GREEN +f'Successfully deleted {file_name}')
    except FileNotFoundError:
        print(Fore.RED +f'{file_name} not found!')
    except Exception as e:
        print(Fore.RED+f'Cannot create file {e}')

'''
This has commands related to directories
'''
#creates a directory
def makedir(cmd):
    dir_name=cmd[5:].strip()
    try:
        os.mkdir(dir_name)
        print(Fore.GREEN +f'Successfully created {dir_name}')
    except FileExistsError:
        print(Fore.YELLOW +f'{dir_name} already exists!!')
    except Exception as e:
        print(Fore.RED+f'Cannot create directory {e}')
    
# deletes a directory
def delete_dir(cmd):
    dir_name=cmd[5:].strip()
    try:
        os.rmdir(dir_name)
        print(Fore.GREEN +f'Successfully deleted {dir_name}')
    except FileNotFoundError:
        print(Fore.RED +f'{dir_name} not found!')
    except Exception as e:
        print(Fore.RED+f'Cannot create file {e}')

# renames directory
def rename(cmd):
    old_name=cmd.split()[1]
    new_name=cmd.split()[2]
    try:
        os.rename(old_name,new_name)
        print(Fore.GREEN +f'Successfully renamed {old_name} -> {new_name}')
    except Exception as e:
        print(Fore.RED+f'(┬┬﹏┬┬)\nSomething is wrong.\n{e}')

# search files and directories
def search(cmd):
    search_term = cmd[7:].strip()
    if not search_term:
        print(Fore.RED + "Please provide a search term!")
        return

    results = []
    try:
        # Traverse the current directory and subdirectories
        for root, dirs, files in os.walk("."):
            for name in dirs + files:
                if search_term.lower() in name.lower():  # Case-insensitive search
                    results.append(os.path.join(root, name))
        
        if results:
            print(Fore.GREEN + f"Found {len(results)} result(s):")
            for result in results:
                print(Fore.CYAN + result)
        else:
            print(Fore.YELLOW + "No matching files or directories found.")
    except Exception as e:
        print(Fore.RED + f"An error occurred while searching: {e}")

