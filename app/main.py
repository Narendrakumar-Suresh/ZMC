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
        if os.path.isdir(directory):  # Ensure it's a valid directory
            try:
                for file in os.listdir(directory):
                    full_path = os.path.join(directory, file)
                    if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                        executables.add(file)  # Add only the filename
            except PermissionError:
                continue  # Ignore directories we can't access
    return executables

def longest_common_prefix(strings):
    """Find the longest common prefix among a list of strings."""
    if not strings:
        return ""
    prefix = strings[0]
    for s in strings[1:]:
        while not s.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    return prefix

def completer(text, state):
    """Autocomplete function for shell commands, filenames, and executables."""
    path_variable = os.environ.get("PATH", "")
    path_dirs = path_variable.split(":") if path_variable else []
    executables = get_executables(path_dirs)  # Refresh executables dynamically

    matches = sorted(cmd for cmd in executables if cmd.startswith(text))
    
    if not matches:
        return None
    
    if len(matches) == 1:
        return matches[0] + ' '
    
    if state == 0:
        sys.stdout.write("\a")  # Ring bell on first TAB press
        sys.stdout.flush()
        return None
    
    if state == 1:
        sys.stdout.write("\n" + "  ".join(matches) + "\n$ ")  # Print matches on second TAB
        sys.stdout.flush()
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
            
            case 'type':
                if not args:
                    continue
                
                args = "".join(args)
                executable_path = find_executable(args, path_dirs)
                
                if args in builtin:
                    sys.stdout.write(f"{args} is a shell builtin\n")
                elif executable_path:
                    sys.stdout.write(f"{args} is {executable_path}\n")
                else:
                    sys.stdout.write(f"{args}: not found\n")
            
            case 'pwd':
                sys.stdout.write(os.getcwd() + '\n')
            
            case 'cd':
                if not args or "".join(args) == '~':
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
