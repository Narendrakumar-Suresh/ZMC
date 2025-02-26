import sys

def main():
    builtin=['echo','exit','type']
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
                args="".join(args)
                if args in builtin:
                    print(f"{args} is a shell builtin")
                else:
                    sys.stdout.write(f'"{args}: command not found\n"')
            case _:
                sys.stdout.write(f"{cmd}: command not found\n")


if __name__ == "__main__":
    main()
