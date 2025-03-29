
import subprocess
import sys

def run_command(command):
    """Runs a system command and returns the output as a list of lines."""
    try:
        output = subprocess.check_output(command, stderr=subprocess.DEVNULL).decode('utf-8', errors="ignore").split('\n')
        return output
    except subprocess.CalledProcessError:
        return []

def get_wifi_profiles():
    """Retrieves all saved Wi-Fi profiles."""
    data = run_command(['netsh', 'wlan', 'show', 'profiles'])
    return [line.split(":")[1].strip() for line in data if "All User Profile" in line]

def get_wifi_password(profile):
    """Retrieves the Wi-Fi password for a given profile."""
    data = run_command(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'])
    for line in data:
        if "Key Content" in line:
            return line.split(":")[1].strip()
    return "N/A"

def is_admin():
    """Checks if the script is running with administrator privileges."""
    try:
        return subprocess.check_output("net session", stderr=subprocess.DEVNULL, shell=True)
    except subprocess.CalledProcessError:
        return False

def main():
    if not is_admin():
        print("[!] Please run this script as an administrator.")
        sys.exit(1)
    
    print("\n{:<30} |  {:<}".format("Wi-Fi Name", "Password"))
    print("-" * 50)
    
    profiles = get_wifi_profiles()
    if not profiles:
        print("[!] No saved Wi-Fi profiles found.")
        return
    
    for profile in profiles:
        password = get_wifi_password(profile)
        print("{:<30} |  {:<}".format(profile, password))

    input("\nPress Enter to exit...")

if __name__== "__main__":
    main()
    
