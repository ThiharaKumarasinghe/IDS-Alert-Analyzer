import tkinter as tk
from tkinter import ttk
import subprocess
import os
import time
import sys
import threading

# from test_1 import RedirectOutput
class RedirectOutput:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)  # Scroll to the end

    def flush(self):
        pass  # This can be implemented if needed


# Window configurations
width = 600
height = 500

# Initialize snort_process variable
snort_process = None

def read_snort_output():
    for i in range(10):  # Simulate 10 alerts
        print(f"Alert {i + 1}: Intrusion detected!")
        time.sleep(2)  # Wait for 2 seconds before generating the next alert
    global snort_process
    if snort_process is not None:
        while True:
            output = snort_process.stdout.readline()
            if output:
                alerts_text.insert(tk.END, output)
                alerts_text.see(tk.END)
            elif snort_process.poll() is not None:
                break
        # Capture stderr in case of errors
        errors = snort_process.stderr.read()
        if errors:
            alerts_text.insert(tk.END, "\nErrors:\n" + errors)

# Function to start Snort
def start_snort():
    try:
        # Change directory to Snort bin
        os.chdir(r"c:\Snort\bin")
        
        # Define the Snort command
        command = ["snort", "-i", "4", "-c", r"c:\Snort\etc\snort.conf", "-A", "console"]
        
        # Start Snort in a subprocess
        global snort_process
        # snort_process = subprocess.Popen(
        #     command,
        #     stdout=subprocess.PIPE,
        #     stderr=subprocess.PIPE,
        #     creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
        #     text=True,
        # )

        snort_process = subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        status_label.config(text="Snort started")
        
        # Start a thread to read Snort output
        threading.Thread(target=read_snort_output).start()
    except Exception as e:
        status_label.config(text=f"An error occurred: {e}")

# Function to stop Snort
def stop_snort():
    global snort_process
    if snort_process:
        try:
            # Forcefully kill the Snort process
            snort_process.kill()  # Forcefully terminate the process
            snort_process.wait()  # Ensure the process has terminated
            status_label.config(text="Snort stopped")
            snort_process = None  # Reset the snort_process variable
        except Exception as e:
            status_label.config(text=f"An error occurred while stopping Snort: {e}")

# Function to close the application
def close_app():
    stop_snort()  # Ensure Snort is stopped when closing the app
    root.destroy()

# Create the main window
root = tk.Tk()
root.title("IDS Alert Analyser")
root.geometry(f'{width}x{height}')

# Create status label
status_label = ttk.Label(root, text="Status: Idle")
status_label.pack(pady=10)

# Create text widget to display alerts
alerts_text = tk.Text(root, wrap='word', height=20, width=70)
alerts_text.pack(pady=10, padx=10)

# Redirect stdout to the Text widget
sys.stdout = RedirectOutput(alerts_text)

# Create buttons
start_button = ttk.Button(root, text="Start Snort", command=start_snort)
stop_button = ttk.Button(root, text="Stop Snort", command=stop_snort)
close_button = ttk.Button(root, text="Close", command=close_app)

# Position buttons on the window
start_button.pack(pady=5)
stop_button.pack(pady=5)
close_button.pack(pady=5)

# Start the application
root.mainloop()
