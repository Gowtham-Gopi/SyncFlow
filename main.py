import os
import sys
import json
from datetime import datetime
import compressor

config_template = {
    "source": "C:/folder/Backups/",
    "destination": "G:/My Drive/",
    "folder_name": "Backups"
}

def clear_screen():
    """Cleans up the console screen for a fresh layout template."""
    os.system('cls' if os.name == 'nt' else 'clear')

def create_config(BASE_DIR):
    try:
        config_path = os.path.join(BASE_DIR, "config.json")
        with open(config_path, "w+") as file:
            json.dump(config_template, file, indent=4)
    except Exception as e:
        print(f"Error {e}")

def load_config():
    """Dynamically loads configuration right next to the running executable."""
    if getattr(sys, 'frozen', False):
        BASE_DIR = os.path.dirname(sys.executable)
    else:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        
    config_path = os.path.join(BASE_DIR, "config.json")
    
    try:
        with open(config_path, "r") as f:
            return json.load(f), BASE_DIR
    except FileNotFoundError:
        clear_screen()
        print("=" * 60)
        print(" CRITICAL ERROR: CONFIGURATION MISSING ".center(60, "!"))
        print("=" * 60)
        print(f"\n❌ Cannot find 'config.json' at:\n   {config_path}")
        create_config(BASE_DIR)
        print("\n👉 A CONFIG TEMPLATE IS CREATED. EDIT THAT FILE TO PROCEED.")
        print("=" * 60)
        input("\nPress [ENTER] to exit...")
        sys.exit(1)


def upload_via_desktop_client():
    config, base_dir = load_config()
    
    # source_folder = config["source"]
    # g_drive_path = config["destination"]
    # folder_name = config["folder_name"]

    config_source = config.get("source")       # "C:/Users/gowth/Downloads/Backups"
    config_dest = config.get("destination")    # "G:/My Drive"
    folder_name = config.get("folder_name")    # "Backups"

    source_folder = os.path.normpath(config_source)

    if not os.path.exists(os.path.normpath(config_dest)):
        print("\n❌ Error: Virtual 'G:/My Drive/backups' stream destination not found.")
        print("👉 Please make sure Google Drive for Desktop application is actively running.")
        print("=" * 60)
        input("\nPress [ENTER] to close...")
        return

    backup_destination = os.path.normpath(os.path.join(config_dest, folder_name))

    if not os.path.exists(backup_destination):
        print("Backup Folder does not exist. Creating a new folder !")
        os.makedirs(backup_destination)

    if not os.path.exists(source_folder):
        print("\n❌ Error: Source folder does not exist.")
        print("=" * 60)
        input("\nPress [ENTER] to close...")
        return

    # List Todays Backups
    today_date = datetime.now().date()
    clear_screen()
    print("=" * 60)
    print(" GOOGLE DRIVE AUTOMATED BACKUP SYSTEM ".center(60, "█"))
    print("=" * 60)
    print(f" 📂 SOURCE:      {source_folder}")
    print(f" 🎯 DESTINATION: {backup_destination}")
    print("-" * 60)

    print("🔍 Indexing structural files, please wait...")
    
    folder_count = 0
    latest_folder = ""
    latest_creation = ""

    for i in os.listdir(source_folder):
        full_path = os.path.join(source_folder, i)

        if os.path.isdir(full_path):

            creation_time = os.path.getctime(full_path)
            creation_time = datetime.fromtimestamp(creation_time)

            if creation_time.date() == today_date:
                folder_count+=1
                if latest_folder == "" or latest_creation < creation_time:
                    latest_creation = creation_time
                    latest_folder = full_path



    if folder_count == 0:
        print("-" * 60)
        print("\n ⚠️  STATUS: NO LOCAL BACKUPS DETECTED FOR TODAY \n")
        print(f" 👉 Reason: Your local ERP system has not generated any new ")
        print(f"    backup folders today ({today_date}).")
        print("\n 👉 Action Required: ")
        print("    1. Open your main ERP accounting/billing software.")
        print("    2. Run a manual 'Local Backup' first.")
        print("    3. Once the local backup is complete, relaunch this app.\n")
        return

    elif folder_count > 1:

        latest_folder_name = os.path.basename(latest_folder)

        print(f"Number of Backups found for today's date: {folder_count}\n")
        print("Compressing latest backup")
        print(f"Latest: {latest_folder_name} at {latest_creation.strftime("%I:%M %p")}\n")
    
    try:
        latest_folder_name = os.path.basename(latest_folder)
        compressor.zip_folder(backup_destination, latest_folder, latest_folder_name+".zip")
    except Exception as e:
        print(f"Error {e}")

if __name__ == "__main__":
    upload_via_desktop_client()
    pause = input("Press any button to exit....")