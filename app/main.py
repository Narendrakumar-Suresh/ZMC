from collections.abc import Mapping
import readline
import shlex
import subprocess
import sys
import pathlib
import os
from typing import Final, TextIO

SHELL_BUILTINS: Final[list[str]] = [
    "echo",
    "exit",
    "type",
    "pwd",
    "cd",
]

def parse_programs_in_path(path: str, programs: dict[str, pathlib.Path]) -> None:
    """Creates a mapping of programs in path to their paths"""
    # Note: Using .walk() instead of .rglob() per the reference.
    for p, _, bins in pathlib.Path(path).walk():
        for b in bins:
            programs[b] = p / b

def generate_program_paths() -> Mapping[str, pathlib.Path]:
    programs: dict[str, pathlib.Path] = {}
    for p in (os.getenv("PATH") or "").split(":"):
        parse_programs_in_path(p, programs)
    return programs

PROGRAMS_IN_PATH: Final[Mapping[str, pathlib.Path]] = {**generate_program_paths()}
COMPLETIONS: Final[list[str]] = [*SHELL_BUILTINS, *PROGRAMS_IN_PATH.keys()]

# Global state for tab completion.
tab_press_count: int = 0
previous_text: str = ""

def complete(text: str, state: int) -> str | None:
    """
    If there's exactly one match, return it immediately (with a trailing space).
    If there are multiple matches:
      - On the first TAB press, just ring the bell.
      - On the second TAB press, print all matching commands separated by 2 spaces,
        then reprint the prompt with the current text.
    For subsequent calls (state > 0), cycle through the matches.
    """
    global tab_press_count, previous_text

    # Build list of matching completions.
    matches = sorted([s for s in COMPLETIONS if s.startswith(text)])
    
    # Reset tab count if text has changed.
    if text != previous_text:
        previous_text = text
        tab_press_count = 0

    # If no matches, return None.
    if not matches:
        return None

    # If exactly one match, always return that (only on state==0).
    if len(matches) == 1:
        return matches[0] + " " if state == 0 else None

    # If there are multiple matches:
    if state == 0:
        tab_press_count += 1
        if tab_press_count == 1:
            # First TAB press: ring the bell.
            sys.stdout.write("\a")
            sys.stdout.flush()
            return None
        elif tab_press_count == 2:
            # Second TAB press: print all matches (joined by two spaces) and reprint prompt.
            print()  # Move to a new line.
            print("  ".join(matches))
            # Reprint the prompt with current text (without a trailing newline).
            sys.stdout.write("$ " + text)
            sys.stdout.flush()
            return None
    # For cycling through matches, return the match corresponding to state.
    if state < len(matches):
        return matches[state] + " "
    return None

# (Optional) We disable the default display hook since we handle display ourselves.
readline.set_completion_display_matches_hook(None)
readline.parse_and_bind("tab: complete")
readline.set_completer(complete)

def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        try:
            line = input()
        except EOFError:
            break
        cmds = shlex.split(line)
        out: TextIO = sys.stdout
        err: TextIO = sys.stderr
        close_out = False
        close_err = False
        try:
            if ">" in cmds:
                out_index = cmds.index(">")
                out = open(cmds[out_index + 1], "w")
                close_out = True
                cmds = cmds[:out_index] + cmds[out_index + 2 :]
            elif "1>" in cmds:
                out_index = cmds.index("1>")
                out = open(cmds[out_index + 1], "w")
                close_out = True
                cmds = cmds[:out_index] + cmds[out_index + 2 :]
            if "2>" in cmds:
                out_index = cmds.index("2>")
                err = open(cmds[out_index + 1], "w")
                close_err = True
                cmds = cmds[:out_index] + cmds[out_index + 2 :]
            if ">>" in cmds:
                out_index = cmds.index(">>")
                out = open(cmds[out_index + 1], "a")
                close_out = True
                cmds = cmds[:out_index] + cmds[out_index + 2 :]
            elif "1>>" in cmds:
                out_index = cmds.index("1>>")
                out = open(cmds[out_index + 1], "a")
                close_out = True
                cmds = cmds[:out_index] + cmds[out_index + 2 :]
            if "2>>" in cmds:
                out_index = cmds.index("2>>")
                err = open(cmds[out_index + 1], "a")
                close_err = True
                cmds = cmds[:out_index] + cmds[out_index + 2 :]
            handle_all(cmds, out, err)
        finally:
            if close_out:
                out.close()
            if close_err:
                err.close()

def handle_all(cmds: list[str], out: TextIO, err: TextIO):
    match cmds:
        case ["echo", *s]:
            out.write(" ".join(s) + "\n")
        case ["type", s]:
            type_command(s, out, err)
        case ["exit", "0"]:
            sys.exit(0)
        case ["pwd"]:
            out.write(f"{os.getcwd()}\n")
        case ["cd", dir]:
            cd(dir, out, err)
        case [cmd, *args] if cmd in PROGRAMS_IN_PATH:
            process = subprocess.Popen([cmd, *args], stdout=out, stderr=err)
            process.wait()
        case command:
            out.write(f"{' '.join(command)}: command not found\n")

def type_command(command: str, out: TextIO, err: TextIO):
    if command in SHELL_BUILTINS:
        out.write(f"{command} is a shell builtin\n")
        return
    if command in PROGRAMS_IN_PATH:
        out.write(f"{command} is {PROGRAMS_IN_PATH[command]}\n")
        return
    out.write(f"{command}: not found\n")

def cd(path: str, out: TextIO, err: TextIO) -> None:
    if path.startswith("~"):
        home = os.getenv("HOME") or "/root"
        path = path.replace("~", home)
    p = pathlib.Path(path)
    if not p.exists():
        out.write(f"cd: {path}: No such file or directory\n")
        return
    os.chdir(p)

if __name__ == "__main__":
    main()
