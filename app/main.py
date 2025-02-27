import sys
import os
import subprocess
import shlex

def find_executable(command, path_dirs):
    """Search for an executable in the PATH directories."""
    for directory in path_dirs:
        full_path = os.path.join(directory, command)
        if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
            return full_path
    return None

def execute_command(command):
    """Execute a command with optional output redirection."""
    parts = shlex.split(command, posix=True)
    if '>' in parts or '1>' in parts:
        # Identify redirection operator and split command
        if '>' in parts:
            op_index = parts.index('>')
        else:
            op_index = parts.index('1>')
        
        cmd_parts = parts[:op_index]  # Command and arguments
        file_name = parts[op_index + 1] if op_index + 1 < len(parts) else None
        
        if not file_name:
            sys.stdout.write("Error: No output file specified\n")
            return
        
        try:
            with open(file_name, 'w') as output_file:
                subprocess.run(cmd_parts, env=os.environ, stdout=output_file, stderr=sys.stderr, check=False)
        except Exception as e:
            sys.stdout.write(f"Error: {e}\n")
    else:
        subprocess.run(parts, env=os.environ, check=False)

def main():
    builtin = ['echo', 'exit', 'type', 'pwd', 'cd']
    path_variable = os.environ.get("PATH", "")
    path_dirs = path_variable.split(":") if path_variable else []
    
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        command = input().strip()
        
        if not command:
            continue
        
        var = shlex.split(command, posix=True)
        cmd = var[0]
        args = var[1:]
        
        if '>' in args or '1>' in args:
            execute_command(command)
            continue
        
        match cmd:
            case "exit":
                break
            
            case "echo":
                if '>' in args or '1>' in args:
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