import sys

def main():
    while True:
        sys.stdout.write("$ ")

        # Wait for user input
        command=input().split()
        cmd = command[0]
        args = command[1:]
        # print(f'This is the command: {cmd}')
        
        if cmd == "exit":
            sys.exit(0)
        elif cmd.startswith('echo'):
            sys.stdout.write("".join(args)+'\n')
        else:
            sys.stdout.write(f"{command}: command not found")


if __name__ == "__main__":
    main()
