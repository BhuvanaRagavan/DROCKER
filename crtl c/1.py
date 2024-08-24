import keyboard
import pyperclip
import time
import csv
import os
import subprocess

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

# Function to write the file path to a new CSV file
def write_to_csv(data, filename='clean_file_paths.csv'):
    with open(filename, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(data)

# Function to monitor keyboard for Ctrl+C and log file path
def monitor_keyboard():
    print("Monitoring for Ctrl+C. Press Ctrl+C to log the file path.")
    while True:
        try:
            if keyboard.is_pressed('ctrl+c'):
                # Wait for the Ctrl+C key combination to be released
                time.sleep(0.1)
                # Retrieve the file path from the clipboard
                file_path = get_clean_file_path_from_powershell()
                if file_path:
                    write_to_csv([file_path])
                    print(f"File path logged: {file_path}")
                else:
                    print("No file path found or path could not be retrieved.")
                # Wait a bit before checking again to avoid multiple logs for the same key press
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopped monitoring.")
            break

if __name__ == "__main__":
    # Ensure the CSV file has headers if it doesn't exist
    if not os.path.exists('clean_file_paths.csv'):
        with open('clean_file_paths.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["File Path"])

    monitor_keyboard()
