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
    """Finds the longest common prefix of a list of strings."""
    if not strings:
        return ""
    prefix = strings[0]
    for string in strings[1:]:
        while not string.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    return prefix

previous_completion_text = None
tab_press_count = 0

def completer(text, state):
    """Autocomplete function for shell commands, filenames, and executables."""
    global previous_completion_text, tab_press_count

    # Get executables from PATH
    path_variable = os.environ.get("PATH", "")
    path_dirs = path_variable.split(":") if path_variable else []
    executables = get_executables(path_dirs)

    # Include built-in commands in autocomplete
    all_commands = builtin + list(executables)

    # Get possible matches
    options = sorted(cmd for cmd in all_commands if cmd.startswith(text))

    # Reset tab_press_count if the text has changed
    if text != previous_completion_text:
        previous_completion_text = text
        tab_press_count = 0

    # Handle longest common prefix completion
    if options:
        common_prefix = longest_common_prefix(options)

        # If there's only one match, complete it and add a space
        if len(options) == 1:
            return options[0] + ' '  # ✅ Fix: Ensure it completes "exit" to "exit "

        # If the common prefix is longer than input, complete it
        if common_prefix != text:
            return common_prefix  # ✅ Partial completion if multiple matches exist

        # First TAB press: Ring the bell
        if tab_press_count == 0:
            sys.stdout.write("\a")  # Ring the bell
            sys.stdout.flush()
            tab_press_count += 1
            return None

        # Second TAB press: Show all matches
        if tab_press_count == 1:
            sys.stdout.write("\n" + "  ".join(options) + "\n")  # Print all matches
            sys.stdout.write("$ " + text)  # Reprint prompt with typed text
            sys.stdout.flush()
            return None

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
