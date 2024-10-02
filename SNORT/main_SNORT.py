import tkinter as tk
from tkinter import ttk
import subprocess
import os

# Window configurations
width = 500
height = 500



# Initialize snort_process variable
snort_process = None

# Function to start Snort
def start_snort():
    try:
        # Change directory to Snort bin
        os.chdir(r"c:\Snort\bin")
        
        # Define the Snort command
        command = ["snort", "-i", "4", "-c", r"c:\Snort\etc\snort.conf", "-A", "console"]
        
        # Start Snort in a subprocess
        global snort_process
        snort_process = subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        print("Snort started")
        status_label.config(text="Snort Started")
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to stop Snort
def stop_snort():
    global snort_process
    if snort_process:
        try:
            # Forcefully kill the Snort process
            snort_process.kill()  # Forcefully terminate the process
            snort_process.wait()  # Ensure the process has terminated
            status_label.config(text="Snort stopped")
            print("Snort stopped")
            snort_process = None  # Reset the snort_process variable
        except Exception as e:
            print(f"An error occurred while stopping Snort: {e}")

# Function to close the application
def close_app():
    stop_snort()  # Ensure Snort is stopped when closing the app
    root.destroy()

# Create the main window
root = tk.Tk()
root.title("IDS Alert Analyser")
root.geometry(f'{width}x{height}')

# Create status label
status_label = ttk.Label(root, text="Status of the SNORT")
status_label.pack(pady=10)


# Create buttons
start_button = ttk.Button(root, text="Start Snort", command=start_snort)
stop_button = ttk.Button(root, text="Stop Snort", command=stop_snort)
close_button = ttk.Button(root, text="Close", command=close_app)

# Position buttons on the window
start_button.pack(pady=10)
stop_button.pack(pady=10)
close_button.pack(pady=10)

# Start the application
root.mainloop()
