import subprocess
import sys

def install_requirements():
    try:
        subprocess.check_call([sys.executable, "-m", "pip3", "install", "-r", "requirements.txt"])
        print("All dependencies installed successfully!")
    except subprocess.CalledProcessError:
        print("An error occurred while installing dependencies.")
        sys.exit(1)

if __name__ == "__main__":
    install_requirements()