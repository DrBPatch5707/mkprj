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

def init_git(args):
	path = os.path.join(os.path.abspath(args.path), args.name)
	if not args.no_git:	
		try:
			result = subprocess.run(["git", "init", path], capture_output=True, text=True, check=True)
			Info("")
			print(result.stdout)
			print(result.stderr)
		except subprocess.CalledProcessError as e:
			Error(f"Git initalization of repo {path} failed do to error code {e.returncode}")

def copy_template(inPath, outPath):
	try:
		with open(inPath, "r") as file:
			contents = file.read()
	except FileNotFoundError:
		Error(f"Could not read the {inPath} template")
		abort()
	except OSError as ec:
		Error(f"The host operating system raised error code {ec.errno}")
		abort()
	except Exception as e:
		Error(f"Unexpected error reading {inPath} template: {e}")
		abort()
	Info(f"Creating {outPath}...")
	try:
		with open(outPath, "w") as file:
			file.write(contents)
	except FileNotFoundError:
		Error(f"Could not create {outPath}")
		abort()
	except OSError as ec:
		Error(f"The host operating system rased error code {ec.errno}")
		abort()
	except Exception as e:
		Error(f"Unexpected error writing {outPath}: {e}")
		abort()

def create_project_dir(path):
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

#Profiles---------------


def default_profile(args):
	pth = os.path.join(os.path.abspath(args.path), args.name)
	create_project_dir(pth)
	init_git(args)
	create_src_dir(pth)



def rust_profile(args):
	path = os.path.join(os.path.abspath(args.path), args.name)
	try:
		result = subprocess.run(["cargo", "new", path], capture_output=True, text=True, check=True)
		Info("")
		print(result.stdout)
		print(result.stderr)
	except subprocess.CalledProcessError as e:
		Error(f"Cargo initalization of {path} failed do to error code {e.returncode}")
	init_git(args)
	#More later

def cpp_profile(args):
	pth = os.path.join(os.path.abspath(args.path), args.name)
	create_project_dir(pth)
	init_git(args)
	copy_template(
		inPath=os.path.join(TEMPLATE_DIR, "cpp_Makefile_.txt"),
		outPath=os.path.join(pth, "Makefile")
	)
	src_path = create_src_dir(pth)
	create_include_dir(pth)
	copy_template(
		inPath=os.path.join(TEMPLATE_DIR, "cpp_main.cpp_.txt"),
		outPath=os.path.join(src_path, "main.cpp")
	)


def cpp_cmake_profile(args):
	pth = os.path.join(os.path.abspath(args.path), args.name)
	create_project_dir(pth)
	init_git(args)
	copy_template(
		inPath=os.path.join(TEMPLATE_DIR, "cpp-cmake_CMakeLists.txt_.txt"),
		outPath=os.path.join(pth, "CMakeLists.txt")
	)
	src_path = create_src_dir(pth)
	create_include_dir(pth)
	copy_template(
		inPath=os.path.join(TEMPLATE_DIR, "cpp-cmake_main.cpp_.txt"),
		outPath=os.path.join(src_path, "main.cpp")
	)
	
def cpp_baremetal_grub_profile(args):
	pth = os.path.join(os.path.abspath(args.path), args.name)
	create_project_dir(pth)
	init_git(args)
	copy_template(
		inPath=os.path.join(TEMPLATE_DIR, "cpp-baremetal-grub_Makefile_.txt"),
		outPath=os.path.join(pth, "Makefile")
	)
	copy_template(
		inPath=os.path.join(TEMPLATE_DIR, "cpp-baremetal-grub_linker.ld_.txt"),
		outPath=os.path.join(pth, "linker.ld")
	)
	copy_template(
		inPath=os.path.join(TEMPLATE_DIR, "cpp-baremetal-grub_grub.cfg_.txt"),
		outPath=os.path.join(pth, "grub.cfg")
	)
	src_path = create_src_dir(pth)
	create_include_dir(pth)
	copy_template(
		inPath=os.path.join(TEMPLATE_DIR, "cpp-baremetal-grub_multiboot2_header.S_.txt"),
		outPath=os.path.join(src_path, "multiboot2_header.S")
	)
	copy_template(
		inPath=os.path.join(TEMPLATE_DIR, "cpp-baremetal-grub_entry.cpp_.txt"),
		outPath=os.path.join(src_path, "entry.cpp")
	)






#Main---------------
def main(args):
	Info(f"Project name: {args.name}")
	path = os.path.join(os.path.abspath(args.path), args.name)
	Info(f"Path: {path}")
	Info(f"Using {args.profile} profile")	
	match args.profile:
		case 'cpp':
			cpp_profile(args)
		case 'cpp-cmake':
			cpp_cmake_profile(args)
		case 'cpp-baremetal-grub':
			cpp_baremetal_grub_profile(args)
		case 'rust':
			rust_profile(args)
		case 'default':
			default_profile(args)
