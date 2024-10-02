import shutil
from tkinter import filedialog, messagebox
import webbrowser
import subprocess
import os

# Initialize the variable to store the selected file path
PCAP_file = None

# Function to convert PCAP to CSV using CICFlowMeter
def convert_pcap_to_csv(pcap_file):
    output_dir = ".\\Test-Purpose"
    output_file = os.path.join(output_dir, os.path.basename(pcap_file).replace('.pcap', '.csv'))

    # Define the path to your virtual environment's activation script
    venv_activation = os.path.join(".venv", "Scripts", "activate.bat")

    # Command to run within the virtual environment
    command = f'cmd.exe /c "{venv_activation} && cicflowmeter -f \"{pcap_file}\" -c \"{output_file}\""'

    try:
        # Execute the command in the current shell
        subprocess.run(command, shell=True, check=True)
        return output_file
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to convert PCAP to CSV: {e}")
        return None

# Function to upload a PCAP file and convert it
def upload_pcap_file():
    global PCAP_file
    # Open a file dialog to select only .pcap files
    file_path = filedialog.askopenfilename(filetypes=[("PCAP Files", "*.pcap")])
    
    if file_path:
        PCAP_file = file_path
        print(f"Selected PCAP file: {PCAP_file}") 
        
        # Convert the selected PCAP file to CSV
        csv_file = convert_pcap_to_csv(PCAP_file)
        
        if csv_file:
            # Show a message box with the CSV file location
            messagebox.showinfo("Conversion Complete", f"CSV file has been saved to: {csv_file}")
            # Open the React website locally
            run_flask_react()

# run the flask and reat
def run_flask_react():
    try:
        # Start the Flask server (backend)
        flask_process = subprocess.Popen(
            ["python", "server.py"], 
            cwd="C:\\Users\\thiha\\OneDrive - engug.ruh.ac.lk\\Semester-7 (OneDrive)\\EE7802 Undergraduate Project\\Project\\GUI-Post Processing of IDS\\IDS_Alert_Analyser\\backend", 
            shell=True
        )
        print("Flask server started...")
        
        # Start the React frontend
        react_process = subprocess.Popen(
            ["npm", "start"], 
            cwd="C:\\Users\\thiha\\OneDrive - engug.ruh.ac.lk\\Semester-7 (OneDrive)\\EE7802 Undergraduate Project\\Project\\GUI-Post Processing of IDS\\IDS_Alert_Analyser\\front-end",  
            shell=True
        )
        print("React frontend started...")
        
        # Optionally open the default web browser to the React frontend
        webbrowser.open("http://localhost:5173", new=2)
        
        # Show a message to the user
        messagebox.showinfo("Info", "Flask and React servers have started. Opening the web app...")

    except Exception as e:
        # Catch any errors and show a message box
        messagebox.showerror("Error", f"An error occurred: {e}")




# Additional helper functions
def select_file(entry_widget):
    file_path = filedialog.askopenfilename(title="Select a file")
    if file_path:
        entry_widget.delete(0, 'end')
        entry_widget.insert(0, file_path)

def save_file(file_entry):
    file_path = file_entry.get()
    if not file_path:
        messagebox.showwarning("Warning", "Please select a file first!")
        return

    save_path = filedialog.asksaveasfilename(title="Save file as")
    if save_path:
        try:
            shutil.copy(file_path, save_path)
            messagebox.showinfo("Success", "File saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")
