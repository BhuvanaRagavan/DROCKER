import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
import os

# Function to load the encryption key from a file
def load_key(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as key_file:
            return key_file.read()
    else:
        messagebox.showerror("Error", "Encryption key not found.")
        return None

# Function to decrypt the given file
def decrypt_file(file_path, key):
    fernet = Fernet(key)
    try:
        with open(file_path, 'rb') as file:
            encrypted_data = file.read()
        decrypted_data = fernet.decrypt(encrypted_data)
        with open(file_path, 'wb') as file:
            file.write(decrypted_data)
        messagebox.showinfo("Success", f"File decrypted: {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Error decrypting file: {e}")

# Function to open file dialog and get the file path
def browse_file():
    file_path = filedialog.askopenfilename(title="Select a File to Decrypt")
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, file_path)

# Function to open file dialog and get the encryption key file path
def browse_key_file():
    key_file_path = filedialog.askopenfilename(title="Select the Encryption Key File")
    key_file_path_entry.delete(0, tk.END)
    key_file_path_entry.insert(0, key_file_path)

# Function to handle the decryption process
def decrypt():
    file_path = file_path_entry.get()
    key_file_path = key_file_path_entry.get()

    if not file_path:
        messagebox.showwarning("Warning", "Please select the file to decrypt.")
        return

    if not key_file_path:
        messagebox.showwarning("Warning", "Please select the encryption key file.")
        return

    key = load_key(key_file_path)
    if key:
        decrypt_file(file_path, key)

# Setting up the Tkinter GUI
root = tk.Tk()
root.title("File Decryption")

tk.Label(root, text="File to Decrypt:").grid(row=0, column=0, padx=10, pady=10)
file_path_entry = tk.Entry(root, width=50)
file_path_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=browse_file).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Encryption Key File:").grid(row=1, column=0, padx=10, pady=10)
key_file_path_entry = tk.Entry(root, width=50)
key_file_path_entry.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=browse_key_file).grid(row=1, column=2, padx=10, pady=10)

tk.Button(root, text="Decrypt File", command=decrypt).grid(row=2, column=0, columnspan=3, pady=20)

root.mainloop()
