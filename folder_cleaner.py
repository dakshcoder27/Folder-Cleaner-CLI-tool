import os
import shutil
import sys

LOG_FILE = "organize_log.txt"

FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".pptx"],
    "Videos": [".mp4", ".mkv", ".avi"],
    "Archives": [".zip", ".rar"],
    "Programs": [".exe", ".msi"]
}

def organize(folder_path):
    if not os.path.exists(folder_path):
        print("❌ Folder does not exist")
        return

    with open(LOG_FILE, "w") as log:
        moved_files = 0

        for file in os.listdir(folder_path):
            source = os.path.join(folder_path, file)

            if not os.path.isfile(source):
                continue

            destination_folder = "Others"

            for folder, extensions in FILE_TYPES.items():
                if file.lower().endswith(tuple(extensions)):
                    destination_folder = folder
                    break

            target_dir = os.path.join(folder_path, destination_folder)
            os.makedirs(target_dir, exist_ok=True)

            shutil.move(source, os.path.join(target_dir, file))
            log.write(f"{file}|{destination_folder}\n")
            moved_files += 1

    print(f"✅ Organized {moved_files} files successfully.")

def revert(folder_path):
    if not os.path.exists(LOG_FILE):
        print("❌ No log file found. Cannot revert.")
        return

    reverted_files = 0

    with open(LOG_FILE, "r") as log:
        for line in log:
            file, folder = line.strip().split("|")

            source = os.path.join(folder_path, folder, file)
            destination = os.path.join(folder_path, file)

            if os.path.exists(source):
                shutil.move(source, destination)
                reverted_files += 1

    print(f"🔁 Reverted {reverted_files} files successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python folder_cleaner.py <organize|revert> <folder_path>")
        sys.exit(1)

    command = sys.argv[1].lower()
    path = sys.argv[2]

    if command == "organize":
        organize(path)
    elif command == "revert":
        revert(path)
    else:
        print("❌ Invalid command. Use 'organize' or 'revert'.")
