import keyboard
import pyperclip
import time
import csv
import os
import subprocess
from cryptography.fernet import Fernet

# CSV file path
csv_file_path = r"C:\Users\Logesh\Desktop\crtl c\clean_file_paths.csv"
encryption_key_file = r"C:\Users\Logesh\Desktop\key logger\encryption_key.key"

# Function to get the clean file path from PowerShell script
def get_clean_file_path_from_powershell():
    try:
        result = subprocess.run(["powershell", "-File", "get_clean_file_path.ps1"], capture_output=True, text=True)
        file_path = result.stdout.strip()
        if file_path and file_path != "No file path found":
            return file_path
        return None
    except Exception as e:
        print(f"Error running PowerShell script: {e}")
        return None

# Function to write the file path to the CSV file
def write_to_csv(data, filename=csv_file_path):
    with open(filename, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(data)

# Function to load the encryption key from the key file
def load_key():
    if os.path.exists(encryption_key_file):
        with open(encryption_key_file, 'rb') as key_file:
            return key_file.read()
    else:
        print("Encryption key not found.")
        return None

# Function to encrypt the given file
def encrypt_file(file_path):
    key = load_key()
    if not key:
        return
    fernet = Fernet(key)
    try:
        with open(file_path, 'rb') as file:
            file_data = file.read()
        encrypted_data = fernet.encrypt(file_data)
        with open(file_path, 'wb') as file:
            file.write(encrypted_data)
        print(f"File encrypted: {file_path}")
    except Exception as e:
        print(f"Error encrypting file: {e}")

# Function to extract and clean the file path from the stored format
def extract_and_clean_file_path(raw_path):
    try:
        # Extract the directory and file name
        lines = raw_path.splitlines()
        directory_line = next((line for line in lines if line.startswith("Directory:")), None)
        file_name_line = next((line for line in lines if line.strip().startswith("-a----")), None)
        
        if directory_line and file_name_line:
            directory = directory_line.replace("Directory:", "").strip()
            file_name = file_name_line.split()[-1]
            return os.path.join(directory, file_name)
        else:
            return None
    except Exception as e:
        print(f"Error extracting file path: {e}")
        return None

# Function to read the latest path from the CSV and encrypt it
def encrypt_latest_file_in_csv():
    try:
        with open(csv_file_path, 'r') as csvfile:
            rows = list(csv.reader(csvfile))
            if not rows:
                print("CSV file is empty.")
                return
            latest_entry = rows[-1][0]
            file_path = extract_and_clean_file_path(latest_entry)
            if file_path and os.path.exists(file_path):
                encrypt_file(file_path)
            else:
                print(f"File path invalid or file does not exist: {file_path}")
    except Exception as e:
        print(f"Error reading from CSV file: {e}")

# Function to monitor keyboard for Ctrl+C and log file path
def monitor_keyboard():
    print("Monitoring for Ctrl+C. Press Ctrl+C to log the file path.")
    while True:
        try:
            if keyboard.is_pressed('ctrl+c'):
                time.sleep(0.1)
                file_path = get_clean_file_path_from_powershell()
                if file_path:
                    write_to_csv([file_path])
                    print(f"File path logged: {file_path}")
                    # Encrypt the file immediately after logging the path
                    encrypt_latest_file_in_csv()
                else:
                    print("No file path found or path could not be retrieved.")
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopped monitoring.")
            break

if __name__ == "__main__":
    # Ensure the CSV file has headers if it doesn't exist
    if not os.path.exists(csv_file_path):
        with open(csv_file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["File Path"])

    monitor_keyboard()
