import sys

def main():
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
            case _:
                sys.stdout.write(f"{cmd}: command not found\n")


if __name__ == "__main__":
    main()
