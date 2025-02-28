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
    # Display matches on a new line
    sys.stdout.write("\n")
    if matches:
        sys.stdout.write("  ".join(matches) + "\n")
    # Get the current input line and redisplay it with the prompt
    current_line = readline.get_line_buffer()
    sys.stdout.write("$ " + current_line)
    sys.stdout.flush()

def completer(text, state):
    # List of all possible commands (built-ins and executables)
    all_commands = builtin + list(executables)
    matches = [cmd for cmd in all_commands if cmd.startswith(text)]
    matches = sorted(set(matches))  # Remove duplicates and sort
    if state < len(matches):
        if len(matches) == 1:
            return matches[state] + " "  # Add space for unique match
        else:
            return matches[state]  # No space for multiple matches
    return None

def parse_command(command):
    """Parse command to separate arguments and redirection."""
    parts = shlex.split(command, posix=True)
    cmd_args = []
    stdout_file = None
    stderr_file = None
    stdout_append = False
    stderr_append = False
    
    i = 0
    while i < len(parts):
        if parts[i] == '>':
            if i + 1 < len(parts):
                stdout_file = parts[i + 1]
                stdout_append = False
                i += 2
            else:
                raise ValueError("Missing file after '>'")
        elif parts[i] == '>>':
            if i + 1 < len(parts):
                stdout_file = parts[i + 1]
                stdout_append = True
                i += 2
            else:
                raise ValueError("Missing file after '>>'")
        elif parts[i] == '2>':
            if i + 1 < len(parts):
                stderr_file = parts[i + 1]
                stderr_append = False
                i += 2
            else:
                raise ValueError("Missing file after '2>'")
        elif parts[i] == '2>>':
            if i + 1 < len(parts):
                stderr_file = parts[i + 1]
                stderr_append = True
                i += 2
            else:
                raise ValueError("Missing file after '2>>'")
        elif parts[i] == '1>>':
            if i + 1 < len(parts):
                stdout_file = parts[i + 1]
                stdout_append = True
                i += 2
            else:
                raise ValueError("Missing file after '1>>'")
        else:
            cmd_args.append(parts[i])
            i += 1
    
    return cmd_args, stdout_file, stderr_file, stdout_append, stderr_append

def execute_command(cmd_args, stdout_file=None, stderr_file=None, stdout_append=False, stderr_append=False):
    """Execute a command with optional output and error redirection."""
    stdout = subprocess.PIPE if stdout_file is None else open(stdout_file, 'a' if stdout_append else 'w')
    stderr = subprocess.PIPE if stderr_file is None else open(stderr_file, 'a' if stderr_append else 'w')
    
    try:
        process = subprocess.run(
            cmd_args,
            env=os.environ,
            stdout=stdout,
            stderr=stderr,
            check=False
        )
        if stdout == subprocess.PIPE and process.stdout:
            sys.stdout.write(process.stdout.decode())
        if stderr == subprocess.PIPE and process.stderr:
            sys.stderr.write(process.stderr.decode())
    except Exception as e:
        sys.stdout.write(f"Error: {e}\n")
    finally:
        if stdout_file and stdout != subprocess.PIPE:
            stdout.close()
        if stderr_file and stderr != subprocess.PIPE:
            stderr.close()

def main():
    global builtin, executables
    global builtin, executables
    builtin = ['echo', 'exit', 'type', 'pwd', 'cd']
    path_variable = os.environ.get("PATH", "")
    path_dirs = path_variable.split(":") if path_variable else []
    executables = get_executables(path_dirs)  # Function to populate executables
    
    # Set up readline autocompletion
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
        
        try:
            cmd_args, stdout_file, stderr_file, stdout_append, stderr_append = parse_command(command)
            if not cmd_args:
                continue
            cmd = cmd_args[0]
            args = cmd_args[1:]
        except ValueError as e:
            sys.stdout.write(f"Error: {e}\n")
            continue
        
        match cmd:
            case "exit":
                break
            case "echo":
                output = " ".join(args) + "\n"
                if stdout_file:
                    with open(stdout_file, 'a' if stdout_append else 'w') as f:
                        f.write(output)
                else:
                    sys.stdout.write(output)
            case "pwd":
                output = os.getcwd() + "\n"
                if stdout_file:
                    with open(stdout_file, 'a' if stdout_append else 'w') as f:
                        f.write(output)
                else:
                    sys.stdout.write(output)
            case "cd":
                path = args[0] if args else os.path.expanduser("~")
                try:
                    os.chdir(path)
                except Exception as e:
                    if stderr_file:
                        with open(stderr_file, 'a' if stderr_append else 'w') as f:
                            f.write(f"cd: {path}: {e}\n")
                    else:
                        sys.stdout.write(f"cd: {path}: {e}\n")
            case _:
                executable_path = find_executable(cmd, path_dirs)
                if executable_path:
                    execute_command(cmd_args, stdout_file, stderr_file, stdout_append, stderr_append)
                else:
                    error_msg = f"{cmd}: command not found\n"
                    if stderr_file:
                        with open(stderr_file, 'a' if stderr_append else 'w') as f:
                            f.write(error_msg)
                    else:
                        sys.stdout.write(error_msg)

if __name__ == "__main__":
    main()