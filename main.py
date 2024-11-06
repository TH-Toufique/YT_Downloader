import os
import sys
import time
import subprocess
import platform

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

# Function to install missing Python packages
def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        print(f"Installing missing module: {package}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Check and install required packages
install_and_import("yt_dlp")
install_and_import("colorama")

# Now import the installed modules
import yt_dlp
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Function to check if ffmpeg is installed, and install it if missing
def check_and_install_ffmpeg():
    try:
        # Check if ffmpeg is already installed
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(Fore.GREEN + "Let's rock and roll 😎.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Install ffmpeg based on platform
        print(Fore.YELLOW + "FFmpeg is not installed. Installing FFmpeg...")
        if "com.termux" in os.getenv("PREFIX", ""):
            os.system("pkg update && pkg install -y ffmpeg")
        elif os.path.isfile("/etc/os-release"):
            with open("/etc/os-release") as f:
                os_info = f.read().lower()
                if "debian" in os_info or "ubuntu" in os_info:
                    os.system("sudo apt update && sudo apt install -y ffmpeg")
                elif "fedora" in os_info:
                    os.system("sudo dnf install -y ffmpeg")
                elif "arch" in os_info:
                    os.system("sudo pacman -Sy ffmpeg --noconfirm")
                else:
                    print(Fore.RED + "OS not supported for automatic FFmpeg installation.")
                    return False
        else:
            print(Fore.RED + "Unable to determine the operating system for FFmpeg installation.")
            return False
    return True

# Function to check if running in Termux and handle storage permissions
def check_storage_permission():
    if "com.termux" in os.getenv("PREFIX", ""):
        # Check if /storage/emulated/0 is accessible
        if not os.path.isdir("/storage/emulated/0"):
            print(Fore.YELLOW + "Requesting storage permission for Termux...")
            os.system("termux-setup-storage")
        else:
            print(Fore.GREEN + "Storage permission already granted.")
        return "/storage/emulated/0/Music/"
    else:
        return os.path.expanduser("~/Downloads/")

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

# Function to convert .webm to .mp4 using ffmpeg and delete the original .webm
def convert_to_mp4(file_path):
    mp4_path = file_path.rsplit(".", 1)[0] + ".mp4"
    try:
        # Run ffmpeg to convert webm to mp4
        subprocess.run(["ffmpeg", "-i", file_path, "-c:v", "libx264", "-c:a", "aac", "-strict", "experimental", mp4_path], check=True)
        print(Fore.GREEN + f"Converted to MP4: {mp4_path}")
        
        # Delete the original .webm file after conversion
        os.remove(file_path)
        print(Fore.GREEN + f"Deleted original .webm file: {file_path}")
    except subprocess.CalledProcessError:
        print(Fore.RED + "Error converting file to MP4.")
    except OSError as e:
        print(Fore.RED + f"Error deleting original .webm file: {e}")

# Main download function
def download_youtube_content():
    if not check_and_install_ffmpeg():
        print(Fore.RED + "FFmpeg installation failed or is unsupported on this OS. Exiting.😰")
        return
    
    while True:
        print(Fore.CYAN + "Welcome to YouTube Downloader!")
        print(Fore.GREEN + "Choose an option:")
        print(Fore.YELLOW + "1. Download audio at best quality")
        print(Fore.YELLOW + "2. Download video at best quality")
        
        # Prompt user for choice
        choice = input(Fore.CYAN + "Enter your choice (1 or 2): ")
        if choice not in ["1", "2"]:
            print(Fore.RED + "Invalid choice! Please enter 1 or 2.")
            continue
        
        # Prompt user for URL
        url = input(Fore.CYAN + "Enter the YouTube link: ").strip()
        if not url:
            print(Fore.RED + "Invalid link! Please enter a valid YouTube URL.😰")
            continue

        # Set download path based on OS
        download_path = get_download_path()
        print(Fore.GREEN + f"Files will be downloaded to: {download_path}")

        # Define download options based on user choice
        ydl_opts = {
            'format': 'bestaudio/best' if choice == "1" else 'bestvideo+bestaudio',
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}] if choice == "1" else [],
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        }

        # Download process
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(Fore.GREEN + "Starting download...")
                info_dict = ydl.extract_info(url, download=True)
                downloaded_file = ydl.prepare_filename(info_dict)
                print(Fore.GREEN + "Download completed successfully!")
                
                # Only prompt for conversion if a video file was downloaded
                if choice == "2" and downloaded_file.endswith(".webm"):
                    convert = input(Fore.CYAN + "Convert .webm to .mp4? (y/n): ").strip().lower()
                    if convert == 'y':
                        convert_to_mp4(downloaded_file)

        except Exception as e:
            print(Fore.RED + f"Error during download: {e}")

        # Ask user if they want to download more
        more = input(Fore.CYAN + "Do you want to download more? (y/n): ").strip().lower()
        if more != 'y':
            print(Fore.GREEN + "Thank you for using YouTube Downloader. Goodbye!👋")
            break

# Run the downloader
if __name__ == "__main__":
    download_youtube_content()
