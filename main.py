#main.py
import os
import sys
import subprocess

def Info(msg):
	print(f"[INFO] {msg}")

def Error(msg):
	print(f"[ERROR] {msg}")

def Warn(msg):
	print(f"[WARNING] {msg}")


def abort():
	if not hasattr(abort, "aborted"):
		abort.aborted = 0
		Info("aborting...")
	sys.exit()

def init_git(path):
	try:
		result = subprocess.run(["git", "init", path], capture_output=True, text=True)
		Info("")
		print(result.stdout)
		print(result.stderr)
	except subprocess.CalledProcessError as e:
		Error(f"Git initalization of repo {path} failed do to error code {e.returncode}")

def cpp_profile(args):
	pth = os.path.join(os.path.abspath(args.path), args.name)
	Info("Creating Makefile...")
	try:
		with open(os.path.join(pth, "Makefile"), "w") as file:

			contents = r"""
# Compiler and flags
CXX      := g++
CXXFLAGS := -std=c++20 -Wall -Wextra -O2 -Iinclude

# Directories
SRC_DIR   := src
INC_DIR   := include
BUILD_DIR := build

# Target executable name
TARGET := app

# Source and object files
SRCS := $(wildcard $(SRC_DIR)/*.cpp)
OBJS := $(SRCS:$(SRC_DIR)/%.cpp=$(BUILD_DIR)/%.o)

# Default target
all: $(TARGET)

# Link step
$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) $^ -o $@

# Compile step
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.cpp | $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Ensure build directory exists
$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

# Run the program
run: $(TARGET)
	./$(TARGET)

# Clean build artifacts
clean:
	rm -rf $(BUILD_DIR) $(TARGET)

.PHONY: all run clean
"""

			file.write(contents)

			file.close()
	except FileNotFoundError:
		Error("Could not create Makefile")
	except OSError as ec:
		Error(f"The host operating system rased error code {ec.errno}")
		abort()
	except:
		abort()
	
	Info("Creating src directory")
	src_path = os.path.join(pth, "src")
	try:
			os.mkdir(src_path)
	except FileExistsError:
		Error("Somehow the src directory already exist; I don't know man:/")
		abort()
	except FileNotFoundError:
		Error("You shouldn't be here")
		abort()
	except OSError as ec:
		print(f"[INFO] The host operating system has returned error code {ec.errno}")
		abort()
	except:
		abort()

	Info("Creating include directory")
	include_path = os.path.join(pth, "include")
	try:
			os.mkdir(include_path)
	except FileExistsError:
		Error("Somehow the src directory already exist; I don't know man:/")
		abort()
	except FileNotFoundError:
		Error("You shouldn't be here")
		abort()
	except OSError as ec:
		print(f"[INFO] The host operating system has returned error code {ec.errno}")
		abort()
	except:
		abort()
	
	Info("Creating main.cpp...")
	try:
		with open(os.path.join(src_path, "main.cpp"), "w") as file:

			contents = r"""
#include <iostream>

int main() {
	std::cout << "Hello, world" << std::endl;
	return 0;
}
"""

			file.write(contents)

			file.close()
	except FileNotFoundError:
		Error("Could not create Makefile")
	except OSError as ec:
		Error(f"The host operating system rased error code {ec.errno}")
		abort()
	except:
		abort()


def cpp_cmake_profile(args):
	pth = os.path.join(os.path.abspath(args.path), args.name)
	Info("Creating CMakeLists.txt...")
	try:
		with open(os.path.join(pth, "CMakeLists.txt"), "w") as file:

			contents = r"""
cmake_minimum_required(VERSION 3.20)

project(main LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_executable(main)

target_compile_options(main PRIVATE -Wall -Wextra -O2)
target_include_directories(main PRIVATE "${CMAKE_SOURCE_DIR}/include")

file(GLOB APP_SOURCES CONFIGURE_DEPENDS
  "${CMAKE_SOURCE_DIR}/src/*.cpp"
)

target_sources(main PRIVATE ${APP_SOURCES})

set_target_properties(main PROPERTIES
  RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)

add_custom_target(run
  COMMAND "$<TARGET_FILE:main>"
  DEPENDS main
  WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}"
  USES_TERMINAL
)
"""

			file.write(contents)

			file.close()
	except FileNotFoundError:
		Error("Could not create CMakeLists.txt")
	except OSError as ec:
		Error(f"The host operating system rased error code {ec.errno}")
		abort()
	except:
		abort()
	
	Info("Creating src directory")
	src_path = os.path.join(pth, "src")
	try:
			os.mkdir(src_path)
	except FileExistsError:
		Error("Somehow the src directory already exist; I don't know man:/")
		abort()
	except FileNotFoundError:
		Error("You shouldn't be here")
		abort()
	except OSError as ec:
		print(f"[INFO] The host operating system has returned error code {ec.errno}")
		abort()
	except:
		abort()

	Info("Creating include directory")
	include_path = os.path.join(pth, "include")
	try:
			os.mkdir(include_path)
	except FileExistsError:
		Error("Somehow the src directory already exist; I don't know man:/")
		abort()
	except FileNotFoundError:
		Error("You shouldn't be here")
		abort()
	except OSError as ec:
		print(f"[INFO] The host operating system has returned error code {ec.errno}")
		abort()
	except:
		abort()
	
	Info("Creating main.cpp...")
	try:
		with open(os.path.join(src_path, "main.cpp"), "w") as file:

			contents = r"""
#include <iostream>

int main() {
	std::cout << "Hello, world" << std::endl;
	return 0;
}
"""

			file.write(contents)

			file.close()
	except FileNotFoundError:
		Error("Could not create Makefile")
	except OSError as ec:
		Error(f"The host operating system rased error code {ec.errno}")
		abort()
	except:
		abort()


def main(args):
	print(f"[INFO] Project name: {args.name}")
	path = os.path.join(os.path.abspath(args.path), args.name)
	print(f"[INFO] Path: {path}")
	try:
		if os.path.isfile(path):
			print("[ERROR] Directory can not be a file")
			abort()
		if os.path.exists(path):
			print("[ERROR] Directory already exist")
			abort()
		Info(f"Creating directory {path}")
		os.makedirs(path, exist_ok=True)
	except FileExistsError:
		print(f"[ERROR] {path} already exists")
		abort()
	except FileNotFoundError:
		parent = os.path.dirname(path)
		print(f"[ERROR] Parent directory does not exist: {parent}")
		abort()
	except OSError as ec:
		print(f"[INFO] The host operating system has returned error code {ec.errno}")
		abort()
	except:
		abort()

	if not os.path.isdir(path):
		Error("Could not create directory")
		abort()
	
	if not args.no_git:	
		if not os.path.exists(os.path.join(path, ".git")):
			init_git(path)
		else:
			Warn("Git repo exist before initialization; Continuing...")
	

	Info(f"Using profile {args.profile}")
	match args.profile:
		case 'cpp':
			cpp_profile(args)
		case 'cpp-cmake':
			cpp_cmake_profile(args)

			