import sys
import os
import subprocess
import shlex
import readline


def find_executable(command, path_dirs):
    """Search for an executable in the PATH directories."""
    for directory in path_dirs:
        full_path = os.path.join(directory, command)
        if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
            return full_path
    return None


def get_executables(path_dirs):
    """Retrieve all executable files from directories in PATH."""
    executables = set()
    for directory in path_dirs:
        if os.path.isdir(directory):
            try:
                for file in os.listdir(directory):
                    full_path = os.path.join(directory, file)
                    if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                        executables.add(file)
            except PermissionError:
                continue
    return executables


# Variables to track tab completion state
tab_completion_state = {}

def completer(text, state):
    """Autocomplete function for shell commands."""
    path_variable = os.environ.get("PATH", "")
    path_dirs = path_variable.split(":") if path_variable else []
    executables = get_executables(path_dirs)
    options = sorted(cmd for cmd in executables if cmd.startswith(text))
    
    if not options:
        return None  # No matches found
    
    if text not in tab_completion_state:
        tab_completion_state[text] = 0
    
    if tab_completion_state[text] == 0:
        sys.stdout.write("\a")  # Bell sound
        sys.stdout.flush()
        tab_completion_state[text] += 1
        return None
    
    elif tab_completion_state[text] == 1:
        sys.stdout.write("\n" + "  ".join(options) + "\n$ ")
        sys.stdout.flush()
        tab_completion_state[text] = 0
        return None
    
    return None


def main():
    global builtin
    builtin = ['echo', 'exit', 'type', 'pwd', 'cd']
    path_variable = os.environ.get("PATH", "")
    path_dirs = path_variable.split(":") if path_variable else []
    
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")
    
    while True:
        try:
            sys.stdout.write("$ ")
            sys.stdout.flush()
            command = input()
        except EOFError:
            break
        
        if not command:
            continue
        
        var = shlex.split(command, posix=True)
        cmd = var[0]
        args = var[1:]
        
        match cmd:
            case "exit":
                break
            case "echo":
                sys.stdout.write(" ".join(args) + '\n')
            case 'pwd':
                sys.stdout.write(os.getcwd() + '\n')
            case 'cd':
                if not args or args[0] == '~':
                    path = os.path.expanduser('~')
                else:
                    path = args[0]
                try:
                    os.chdir(path)
                except FileNotFoundError:
                    sys.stdout.write(f"cd: {path}: No such file or directory\n")
                except NotADirectoryError:
                    sys.stdout.write(f"cd: {path}: Not a directory\n")
                except PermissionError:
                    sys.stdout.write(f"cd: {path}: Permission denied\n")
            case _:
                executable_path = find_executable(cmd, path_dirs)
                if executable_path:
                    subprocess.run([executable_path] + args, env=os.environ, check=False)
                else:
                    sys.stdout.write(f"{cmd}: command not found\n")


if __name__ == "__main__":
    main()
