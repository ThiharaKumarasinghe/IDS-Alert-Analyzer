import shutil
from tkinter import filedialog, messagebox, Toplevel, Button, Label
import webbrowser
import subprocess
import os

# Initialize the variable to store the selected file path and processes
PCAP_file = None
flask_process = None
react_process = None

# Function to convert PCAP to CSV using CICFlowMeter
def convert_pcap_to_csv(pcap_file):
    output_dir = ".\\CSV_GeneratedFile"
    output_file = os.path.join(output_dir, "alertCSV.csv")

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

# Function to run Flask and React servers
def run_flask_react():
    global flask_process, react_process

    try:
        # Start the Flask server (backend)
        # Define the path to the virtual environment activation script
        venv_activation = os.path.join("C:\\Users\\thiha\\OneDrive - engug.ruh.ac.lk\\Semester-7 (OneDrive)\\EE7802 Undergraduate Project\\Project\\GUI-Post Processing of IDS\\IDS_Alert_Analyser\\backend", ".venv", "Scripts", "activate.bat")

        # Command to navigate to the backend folder, activate the virtual environment, and run Flask server
        flask_command = 'cmd.exe /c "cd ..\\backend && .venv\\Scripts\\activate.bat && python server.py"'


        # Start the Flask server with the virtual environment activated
        flask_process = subprocess.Popen(
            flask_command, 
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
        
        # Open the default web browser to the React frontend
        webbrowser.open("http://localhost:5173", new=2)
        
        # Show the custom message box with Terminate button
        show_terminate_messagebox()

    except Exception as e:
        # Catch any errors and show a message box
        messagebox.showerror("Error", f"An error occurred: {e}")

# Custom message box with Terminate button
def show_terminate_messagebox():
    # Create a new top-level window
    terminate_window = Toplevel()
    terminate_window.title("Info")
    
    # Message label
    label = Label(terminate_window, text="Flask and React servers have started. Opening the web app...")
    label.pack(pady=10)
    
    # Terminate button
    terminate_button = Button(terminate_window, text="Terminate", command=lambda: [terminate_processes(), terminate_window.destroy()])
    terminate_button.pack(pady=10)

    # Set the window size and center it
    terminate_window.geometry("400x150")
    terminate_window.transient()  # Set as a transient window (modal)

    # Make sure the user can only interact with this window
    terminate_window.grab_set()

# Function to terminate both Flask and React processes
def terminate_processes():
    global flask_process, react_process
    if flask_process:
        flask_process.terminate()  # Terminate Flask server
        print("Flask server terminated.")
    if react_process:
        react_process.terminate()  # Terminate React server
        print("React frontend terminated.")
    messagebox.showinfo("Terminated", "Both Flask and React servers have been terminated.")

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
