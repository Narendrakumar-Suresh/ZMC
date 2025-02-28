import sys
import os
import subprocess
import shlex
import readline

tab_press_count = 0
last_completion_text = ""

def find_executable(command, path_dirs):
    for directory in path_dirs:
        full_path = os.path.join(directory, command)
        if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
            return full_path
    return None

def get_executables(path_dirs):
    executables = set()
    for directory in path_dirs:
        if os.path.isdir(directory):
            try:
                for file in os.listdir(directory):
                    full_path = os.path.join(directory, file)
                    if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                        executables.add(file)
            except PermissionError:
                continue
    return executables

def longest_common_prefix(strings):
    if not strings:
        return ""
    prefix = strings[0]
    for string in strings[1:]:
        while not string.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    return prefix

def completer(text, state):
    global tab_press_count, last_completion_text
    path_variable = os.environ.get("PATH", "")
    path_dirs = path_variable.split(":") if path_variable else []
    executables = get_executables(path_dirs)
    options = sorted(cmd for cmd in executables if cmd.startswith(text))
    
    if not options:
        return None
    
    if state == 0:
        if len(options) == 1:
            sys.stdout.write("\r$ " + options[0] + " ")
            sys.stdout.flush()
            readline.insert_text(options[0] + " ")
            readline.redisplay()
            return options[0] + " "
        
        common_prefix = longest_common_prefix(options)
        if common_prefix and common_prefix != text:
            last_completion_text = common_prefix
            sys.stdout.write("\r$ " + common_prefix)
            sys.stdout.flush()
            readline.insert_text(common_prefix)
            readline.redisplay()
            return common_prefix
        
        if tab_press_count == 0:
            tab_press_count += 1
            sys.stdout.write("\a")
            sys.stdout.flush()
            return None
        else:
            sys.stdout.write("\n" + "  ".join(options) + "\n$ " + text)
            sys.stdout.flush()
            tab_press_count = 0
            return None
    return None

def main():
    global builtin
    builtin = ['echo', 'exit', 'type', 'pwd', 'cd']
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")
    while True:
        try:
            sys.stdout.write("$ ")
            sys.stdout.flush()
            command = input()
        except EOFError:
            break
        if not command:
            continue
        
        var = shlex.split(command, posix=True)
        cmd = var[0]
        args = var[1:]
        if cmd == "exit":
            break
        
        if cmd in builtin:
            sys.stdout.write("Built-in command: " + cmd + "\n")
        else:
            executable_path = find_executable(cmd, os.environ.get("PATH", "").split(":"))
            if executable_path:
                subprocess.run([executable_path] + args)
            else:
                sys.stdout.write(f"{cmd}: command not found\n")

if __name__ == "__main__":
    main()
