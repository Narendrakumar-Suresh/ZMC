# ZMC-Zen Mode CLI
> [!WARNING]  
> This is based code-crafters shell. soon more features will be added and still under active development.

## Overview

ZMC-Zen Mode CLI is a minimalistic, efficient command-line shell that provides essential shell functionalities like command execution, redirection, and auto-completion. It aims to provide a distraction-free environment with useful built-in commands and program execution support.

## Features

- **Command Execution:** Supports running system programs and shell built-in commands.
- **Auto-completion:** Uses `readline` for tab-based command suggestions.
- **Redirection:** Supports output and error redirection (`>`, `>>`, `2>`, `2>>`).
- **Built-in Commands:** Implements core shell commands like `echo`, `exit`, `pwd`, `cd`, and `type`.
- **Path Resolution:** Detects available programs from system `$PATH`.

## Built-in Commands

| Command | Description |
|---------|-------------|
| `echo [args]` | Prints the given arguments to stdout. |
| `exit 0` | Exits the shell. |
| `pwd` | Prints the current working directory. |
| `cd [dir]` | Changes the current directory. |
| `type [cmd]` | Identifies if a command is built-in or an executable. |

## Redirection Syntax

| Operator | Description |
|----------|-------------|
| `>` | Redirects stdout to a file (overwrite). |
| `>>` | Redirects stdout to a file (append). |
| `2>` | Redirects stderr to a file (overwrite). |
| `2>>` | Redirects stderr to a file (append). |
| `1>` | Explicitly redirects stdout to a file (overwrite). |
| `1>>` | Explicitly redirects stdout to a file (append). |

## Program Execution

ZMC-Zen Mode CLI supports executing system programs available in the `$PATH`. It first checks if a command is built-in, then searches for an executable.

## Auto-completion

- Uses `readline` for command auto-completion.
- Completes built-in commands and available programs in the `$PATH`.

## Directory Navigation

- `cd ~` navigates to the home directory.
- `cd /path/to/dir` moves to the specified directory.

## Example Usage

```sh
$ echo Hello, World!
Hello, World!

$ pwd
/home/user

$ cd /tmp
$ pwd
/tmp

$ type ls
ls is /bin/ls

$ ls > output.txt  # Redirects output to a file
$ cat output.txt
```

## Installation & Running

1. Clone the repository:

   ```sh
   git clone https://github.com/Narendrakumar-Suresh/ZMC.git
   ```

1. Navigate to the project directory:

   ```sh
   cd ZMC
   ```

2. Run the shell:

   ```sh
   python3 shell.py
   ```

## Contributions

Contributions are welcome! Feel free to submit pull requests or open issues.

## Installation

1. Install my-project with npm

```bash
  git clone https://github.com/yourusername/ZMC.git
```

2. Navigate to the project directory:

```bash
cd ZMC
```

## Roadmap

ZMC is actively being developed! Here are some of the upcoming features:

- **Cross-platform support (Linux, macOS)**: Expanding ZMC's reach to other operating systems.

- **Enhanced Python scripting capabilities**: Improving how Python scripts can be used and integrated with ZMC commands.

- **More custom commands**: We plan to add more useful commands to make the terminal even more powerful.

- **User-friendly configuration options**: Making it easier for users to customize ZMC’s behavior and appearance.

- **Improved performance**: Optimizing the terminal for better speed and responsiveness.

## License

This project is licensed under the MIT License - see the [License](https://github.com/Narendrakumar-Suresh/ZMC/blob/main/LICENSE) file for details.

## Contact

For questions, feedback, or inquiries, feel free to contact us at:

- [Email](narendrkumarsuresh@gmail.com)

- [Twitter](https://x.com/joe_kraper_)
