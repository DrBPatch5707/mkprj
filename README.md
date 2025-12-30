# mkprj

A simple command-line tool to generate boilerplate project structures for various programming languages and build systems.

## Features

- Supports multiple project profiles: `cpp`, `cpp-cmake`.
- Automatically creates directories (e.g., `src`, `include` for C++).
- Initializes a Git repository (unless disabled).
- Uses templates for Makefiles, CMakeLists.txt, and source files.

## Installation

1. Clone or download the repository.
2. Ensure Python 3 is installed.
3. Make the `mkprj` script executable: `chmod +x mkprj`.
4. Optionally, add the script to your PATH for global access.

## Usage

Run the tool with the following syntax:

```bash
./mkprj <profile> <name> [path] [--no-git]
```

- `<profile>`: The project type (e.g., `cpp`, `cpp-cmake`).
- `<name>`: The project name (used as the directory name).
- `[path]`: Optional path where the project will be created (defaults to current directory).
- `--no-git`: Skip Git repository initialization.

### Examples

Create a C++ project with Makefile:

```bash
./mkprj cpp MyCppProject
```

Create a C++ project with CMake in a specific path without Git:

```bash
./mkprj cpp-cmake MyCmakeProject /path/to/projects --no-git
```

## Supported Profiles

- `cpp`: C++ project with Makefile, `src/` and `include/` directories, and a basic `main.cpp`.
- `cpp-cmake`: C++ project with CMake, similar structure but using CMakeLists.txt.
- `cpp-baremetal-grub`: Bare metal C++ application that uses the GRUB bootloader with Multiboot2.
- `rust` : Default profile for rust projects.
- I intend to add more later


## Project Structure

After running, a typical C++ project might look like:

```
MyProject/
├── .git/          # (if Git is initialized)
├── include/       # Header directory
└── src/           # Source directory
    └── main.cpp   # Source files
├── Makefile       # (for cpp profile)
```

## Contributing

Feel free to submit issues or pull requests for new profiles or improvements.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.


## PS:

This README.md was generated using AI with minor edits by me
