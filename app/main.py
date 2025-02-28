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

completion_attempt = 0

def completer(text, state):
    """Autocomplete function for shell commands, filenames, and executables."""
    path_variable = os.environ.get("PATH", "")
    path_dirs = path_variable.split(":") if path_variable else []
    executables = get_executables(path_dirs)  # Refresh executables dynamically

    # Collect possible completions
    options = sorted(cmd for cmd in builtin + list(executables) + os.listdir('.') if cmd.startswith(text))
    
    if state == 0:
        if len(options) > 1:
            sys.stdout.write("\a")  # Ring the bell on first TAB press
            sys.stdout.flush()
            return None
        elif len(options) == 1:
            return options[0] + ' '  # Append space for single match

    if state == 1 and len(options) > 1:
        sys.stdout.write("\n" + "  ".join(options) + "\n")  # Print all matches
        sys.stdout.write("$ " + text)  # Redisplay prompt with the typed text
        sys.stdout.flush()
        return None
    
    if state < len(options):
        return options[state] + ' '
    
    return None

def execute_command(command):
    """Execute a command with optional output and error redirection."""
    parts = shlex.split(command, posix=True)
    try:
        subprocess.run(parts, env=os.environ, check=False)
    except Exception as e:
        sys.stdout.write(f"Error: {e}\n")

def main():
    global builtin
    builtin = ['echo', 'exit', 'type', 'pwd', 'cd']
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
                path = args[0] if args else os.path.expanduser('~')
                try:
                    os.chdir(path)
                except Exception as e:
                    sys.stdout.write(f"cd: {path}: {e}\n")
            case _: 
                executable_path = find_executable(cmd, os.environ.get("PATH", "").split(":"))
                if executable_path:
                    execute_command(command)
                else:
                    sys.stdout.write(f"{cmd}: command not found\n")

if __name__ == "__main__":
    main()