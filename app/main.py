import sys

def main():
    while True:
        sys.stdout.write("$ ")

        # Wait for user input
        command=input()
        li=command.split()
        if li[0]=='exit':
            break
        print(f"{command}: command not found")


if __name__ == "__main__":
    main()
