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

def completer(text, state):
    """Autocomplete function for shell commands and filenames."""
    options = [cmd for cmd in builtin + os.listdir('.') if cmd.startswith(text)]
    if state < len(options):
        return options[state]
    return None

def execute_command(command):
    """Execute a command with optional output and error redirection."""
    parts = shlex.split(command, posix=True)
    stdout_target = None
    stderr_target = None
    stdout_append = False
    stderr_append = False
    
    if '>' in parts or '1>' in parts or '2>' in parts or '>>' in parts or '1>>' in parts or '2>>' in parts:
        cmd_parts = []
        i = 0
        while i < len(parts):
            if parts[i] in {'>', '1>'} and i + 1 < len(parts):
                stdout_target = parts[i + 1]
                i += 2
            elif parts[i] == '2>' and i + 1 < len(parts):
                stderr_target = parts[i + 1]
                i += 2
            elif parts[i] in {'>>', '1>>'} and i + 1 < len(parts):
                stdout_target = parts[i + 1]
                stdout_append = True
                i += 2
            elif parts[i] == '2>>' and i + 1 < len(parts):
                stderr_target = parts[i + 1]
                stderr_append = True
                i += 2
            else:
                cmd_parts.append(parts[i])
                i += 1
        
        if not cmd_parts:
            sys.stdout.write("Error: No command specified\n")
            return
        
        stdout_mode = 'a' if stdout_append else 'w'
        stderr_mode = 'a' if stderr_append else 'w'
        stdout_file = open(stdout_target, stdout_mode) if stdout_target else None
        stderr_file = open(stderr_target, stderr_mode) if stderr_target else None
        
        try:
            subprocess.run(cmd_parts, env=os.environ, stdout=stdout_file or sys.stdout, stderr=stderr_file or sys.stderr, check=False)
        except Exception as e:
            sys.stdout.write(f"Error: {e}\n")
        finally:
            if stdout_file:
                stdout_file.close()
            if stderr_file:
                stderr_file.close()
    else:
        subprocess.run(parts, env=os.environ, check=False)

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
            command = input().strip()
        except EOFError:
            break
        
        if not command:
            continue
        
        var = shlex.split(command, posix=True)
        cmd = var[0]
        args = var[1:]
        
        if '>' in args or '1>' in args or '2>' in args or '>>' in args or '1>>' in args or '2>>' in args:
            execute_command(command)
            continue
        
        match cmd:
            case "exit":
                break
            
            case "echo":
                if '>' in args or '1>' in args or '2>' in args or '>>' in args or '1>>' in args or '2>>' in args:
                    execute_command(command)
                else:
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
                    execute_command(command)
                else:
                    sys.stdout.write(f"{cmd}: command not found\n")

if __name__ == "__main__":
    main()
