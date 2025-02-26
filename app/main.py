import sys

def main():
    while True:
        sys.stdout.write("$ ")

        # Wait for user input
        command=input()

        match command:
            case "exit":
                break
            case "echo":
                args = command.split()[1:]
                print(" ".join(args))
            case _ :
                sys.stdout.write(f"{command}: command not found\n")


if __name__ == "__main__":
    main()
