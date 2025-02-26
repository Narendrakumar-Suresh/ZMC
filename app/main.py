import sys
import os

def find_executable(command, path_dirs):
    """Search for an executable in the PATH directories."""
    for directory in path_dirs:
        full_path = os.path.join(directory, command)
        if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
            return full_path
    return None

def main():
    builtin=['echo','exit','type']
    path_variable = os.environ.get("PATH", "")
    path_dirs = path_variable.split(":") if path_variable else []
    while True:    
        sys.stdout.write("$ ")
        # Wait for user input
        command=input().split()
        cmd = command[0]
        args = command[1:]
        # print(f'This is the command: {cmd}')
        match cmd:
            case "exit":
                break
            case "echo":
                print(" ".join(args))
            case 'type':
                if not args:
                    continue
                args="".join(args)
                executable_path = find_executable(args, path_dirs)

                if executable_path:
                        print(f"{args} is {executable_path}")
                else:
                    print(f"{args}: not found")

            case _:
                sys.stdout.write(f"{cmd}: command not found\n")


if __name__ == "__main__":
    main()
