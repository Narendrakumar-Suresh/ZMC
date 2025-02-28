import sys
import os
import subprocess
import shlex
import readline

# Global variables for command completion
builtin = ['echo', 'exit', 'type', 'pwd', 'cd']
executables = set()

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

def display_matches(substitution, matches, longest_match_length):
    """Display multiple completion matches and redisplay the prompt."""
    sys.stdout.write("\n")
    if matches:
        sys.stdout.write("  ".join(matches) + "\n")
    sys.stdout.write("$ " + substitution)
    sys.stdout.flush()

def completer(text, state):
    """Autocomplete function for shell commands."""
    all_commands = builtin + list(executables)
    matches = [cmd for cmd in all_commands if cmd.startswith(text)]
    matches = sorted(set(matches))  # Remove duplicates and sort
    if state < len(matches):
        if len(matches) == 1:
            return matches[state] + ' '  # Add space for unique match
        else:
            return matches[state]  # No space for multiple matches
    return None

def execute_command(command):
    """Execute a command with optional output and error redirection."""
    parts = shlex.split(command, posix=True)
    try:
        subprocess.run(parts, env=os.environ, check=False)
    except Exception as e:
        sys.stdout.write(f"Error: {e}\n")

def main():
    global builtin, executables
    builtin = ['echo', 'exit', 'type', 'pwd', 'cd']
    # Precompute executables once
    path_variable = os.environ.get("PATH", "")
    path_dirs = path_variable.split(":") if path_variable else []
    executables = get_executables(path_dirs)
    
    # Set up readline for autocompletion
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")
    readline.set_completion_display_matches_hook(display_matches)
    
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
                sys.stdout.write(" ".join(args) + "\n")
            case "pwd":
                sys.stdout.write(os.getcwd() + "\n")
            case "cd":
                path = args[0] if args else os.path.expanduser("~")
                try:
                    os.chdir(path)
                except Exception as e:
                    sys.stdout.write(f"cd: {path}: {e}\n")
            case _:
                executable_path = find_executable(cmd, path_dirs)
                if executable_path:
                    execute_command(command)
                else:
                    sys.stdout.write(f"{cmd}: command not found\n")

if __name__ == "__main__":
    main()