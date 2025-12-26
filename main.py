#main.py
import os
import sys
import subprocess

TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")

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

def create_include_dir(pth):
	Info("Creating include directory")
	include_path = os.path.join(pth, "include")
	try:
			os.mkdir(include_path)
	except FileExistsError:
		Error("Somehow the include directory already exist; I don't know man:/")
		abort()
	except FileNotFoundError:
		Error("You shouldn't be here")
		abort()
	except OSError as ec:
		Error(f"The host operating system has returned error code {ec.errno}")
		abort()
	except:
		abort()
	return include_path
	

def create_src_dir(pth):
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
		Error(f"The host operating system has returned error code {ec.errno}")
		abort()
	except:
		Error("unknown")
		abort()
	return src_path

def init_git(path):
	try:
		result = subprocess.run(["git", "init", path], capture_output=True, text=True, check=True)
		Info("")
		print(result.stdout)
		print(result.stderr)
	except subprocess.CalledProcessError as e:
		Error(f"Git initalization of repo {path} failed do to error code {e.returncode}")

def cpp_profile(args):
	pth = os.path.join(os.path.abspath(args.path), args.name)
	try:
		with open(f"{TEMPLATE_DIR}/cpp_Makefile_.txt", "r") as file:
			contents = file.read()
	except FileNotFoundError as e:
		Error(f"Could not read the Makefile template: {e}")
		abort()
	except OSError as ec:
		Error(f"The host operating system raised error code {ec.errno}")
		abort()
	except Exception as e:
		Error(f"Unexpected error reading Makefile template: {e}")
		abort()
	Info("Creating Makefile...")
	try:
		with open(os.path.join(pth, "Makefile"), "w") as file:
			file.write(contents)
	except FileNotFoundError:
		Error("Could not create Makefile")
	except OSError as ec:
		Error(f"The host operating system rased error code {ec.errno}")
		abort()
	except:
		abort()
	src_path = create_src_dir(pth)
	create_include_dir(pth)
	try:
		with open(f"{TEMPLATE_DIR}/cpp_main.cpp_.txt", "r") as file:
			contents = file.read()
	except FileNotFoundError:
		Error("Could not read the main.cpp template")
		abort()
	except OSError as ec:
		Error(f"The host operating system raised error code {ec.errno}")
		abort()
	except Exception as e:
		Error(f"Unexpected error reading main.cpp template: {e}")
		abort()
	Info("Creating main.cpp...")
	try:
		with open(os.path.join(src_path, "main.cpp"), "w") as file:
			file.write(contents)
	except FileNotFoundError:
		Error("Could not create main.cpp")
	except OSError as ec:
		Error(f"The host operating system rased error code {ec.errno}")
		abort()
	except:
		abort()


def cpp_cmake_profile(args):
	pth = os.path.join(os.path.abspath(args.path), args.name)
	contents = ""
	try:
		with open(f"{TEMPLATE_DIR}/cpp-cmake_CMakeLists.txt_.txt", "r") as file:
			contents = file.read()
	except FileNotFoundError:
		Error("Could not read the CMakeLists.txt template")
		abort()
	except OSError as ec:
		Error(f"The host operating system raised error code {ec.errno}")
		abort()
	except Exception as e:
		Error(f"Unexpected error reading CMakeLists.txt template: {e}")
		abort()

	try:
		with open(os.path.join(pth, "CMakeLists.txt"), "w") as file:
			file.write(contents)
	except FileNotFoundError:
		Error("Could not create CMakeLists.txt")
	except OSError as ec:
		Error(f"The host operating system rased error code {ec.errno}")
		abort()
	except:
		abort()
	
	src_path = create_src_dir(pth)
	create_include_dir(pth)	
	try:
		with open(f"{TEMPLATE_DIR}/cpp-cmake_main.cpp_.txt", "r") as file:
			contents = file.read()
	except FileNotFoundError:
		Error("Could not read the main.cpp template")
		abort()
	except OSError as ec:
		Error(f"The host operating system raised error code {ec.errno}")
		abort()
	except Exception as e:
		Error(f"Unexpected error reading main.cpp template: {e}")
		abort()
	Info("Creating main.cpp...")
	try:
		with open(os.path.join(src_path, "main.cpp"), "w") as file:

			file.write(contents)

			file.close()
	except FileNotFoundError:
		Error("Could not create main.cpp")
	except OSError as ec:
		Error(f"The host operating system rased error code {ec.errno}")
		abort()
	except:
		abort()


def main(args):
	Info(f"Project name: {args.name}")
	path = os.path.join(os.path.abspath(args.path), args.name)
	Info(f"Path: {path}")
	try:
		if os.path.isfile(path):
			Error("Directory can not be a file")
			abort()
		if os.path.exists(path):
			Error("Directory already exist")
			abort()
		Info(f"Creating directory {path}")
		os.makedirs(path)
	except FileExistsError:
		Error(f"{path} already exists")
		abort()
	except FileNotFoundError:
		parent = os.path.dirname(path)
		Error(f"Parent directory does not exist: {parent}")
		abort()
	except OSError as ec:
		Error(f"The host operating system has returned error code {ec.errno}")
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

			