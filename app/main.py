import sys

def main():
    while True:
        sys.stdout.write("$ ")

        # Wait for user input
        command=input()
        
        if command == "exit 0":
            sys.exit(0)
        if command.startswith('echo'):
            print(command[5:].strip())
        print(f"{command}: command not found")


if __name__ == "__main__":
    main()
