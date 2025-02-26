import sys

def main():
    while True:
        sys.stdout.write("$ ")

        # Wait for user input
        command=input()
        cmd = command[0]
        args = command[1:]
        
        if cmd == "exit":
            sys.exit(0)
        elif cmd=='echo':
            sys.stdout.write(args)
        else:
            sys.stdout.write(f"{command}: command not found")


if __name__ == "__main__":
    main()
