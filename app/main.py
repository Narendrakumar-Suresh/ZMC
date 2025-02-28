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

def longest_common_prefix(strings):
    """Find the longest common prefix in a list of strings."""
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
    """Autocomplete function for shell commands and executables."""
    path_variable = os.environ.get("PATH", "")
    path_dirs = path_variable.split(":") if path_variable else []
    executables = get_executables(path_dirs)
    
    options = sorted(cmd for cmd in executables if cmd.startswith(text))
    
    if state == 0:
        completer.match_count = len(options)
        if completer.match_count > 1:
            sys.stdout.write('\a')  # Ring the bell on first TAB
            sys.stdout.flush()
    
    if state < len(options):
        return options[state] + ' '
    
    if state == 1 and completer.match_count > 1:
        sys.stdout.write("\n" + "  ".join(options) + "\n$ ")
        sys.stdout.flush()
    return None

readline.set_completer(completer)
readline.parse_and_bind("tab: complete")

def main():
    while True:
        try:
            sys.stdout.write("$ ")
            sys.stdout.flush()
            command = input()
        except EOFError:
            break
        
        if not command:
            continue
        
        parts = shlex.split(command, posix=True)
        cmd = parts[0]
        args = parts[1:]
        
        executable_path = find_executable(cmd, os.environ.get("PATH", "").split(":"))
        
        if executable_path:
            subprocess.run([executable_path] + args, env=os.environ, check=False)
        else:
            sys.stdout.write(f"{cmd}: command not found\n")

if __name__ == "__main__":
    main()
