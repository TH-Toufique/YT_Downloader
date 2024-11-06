import os
import sys
import time
import subprocess
import platform
import yt_dlp
from colorama import Fore, Style, init
# Banner function
def WriteText(z):
    for e in z + '\n':
        sys.stdout.write(e)
        sys.stdout.flush()
        time.sleep(0.002)
        
time.sleep(0.1)
banner = """\033[096m
██╗   ██╗████████╗    ██████╗  ██████╗ ██╗    ██╗███╗   ██╗██╗      ██████╗  █████╗ ██████╗ ███████╗██████╗ 
╚██╗ ██╔╝╚══██╔══╝    ██╔══██╗██╔═══██╗██║    ██║████╗  ██║██║     ██╔═══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
 ╚████╔╝    ██║       ██║  ██║██║   ██║██║ █╗ ██║██╔██╗ ██║██║     ██║   ██║███████║██║  ██║█████╗  ██████╔╝
  ╚██╔╝     ██║       ██║  ██║██║   ██║██║███╗██║██║╚██╗██║██║     ██║   ██║██╔══██║██║  ██║██╔══╝  ██╔══██╗
   ██║      ██║       ██████╔╝╚██████╔╝╚███╔███╔╝██║ ╚████║███████╗╚██████╔╝██║  ██║██████╔╝███████╗██║  ██║
   ╚═╝      ╚═╝       ╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                                                                            By Ancient Modder"""
WriteText(banner)


# Functions to check and intall missing modules
def install_and_import(package):
    try:
        import(package)
    except ImportError:
        print(f"Installing missing modules: {package}")
        subprocess.check_call([sys.executable, "-m", "pip", "install" ,package])
        
#Check and install missing package
install_and_import("yt_dlp")
install_and_import("colorama")

# Function to determine OS and set download path
def get_download_path():
    # Check for Termux
    if "com.termux" in os.getenv("PREFIX", ""):
        return check_storage_permission()
    # Check for Linux distros based on their IDs in os-release
    elif os.path.isfile("/etc/os-release"):
        with open("/etc/os-release") as f:
            os_info = f.read()
            if "debian" in os_info or "ubuntu" in os_info or "arch" in os_info or "fedora" in os_info:
                return os.path.expanduser("~/Downloads/")
    # Default to Downloads in case of other or unknown OS
    return os.path.expanduser("~/Downloads/")



