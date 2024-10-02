import tkinter as tk
import sys
import threading
import time

class RedirectOutput:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)  # Scroll to the end

    def flush(self):
        pass  # This can be implemented if needed

def generate_alerts():
    for i in range(10):  # Simulate 10 alerts
        print(f"Alert {i + 1}: Intrusion detected!")
        time.sleep(2)  # Wait for 2 seconds before generating the next alert

def start_alerts_thread():
    alert_thread = threading.Thread(target=generate_alerts)
    alert_thread.start()

# Set up the Tkinter window
root = tk.Tk()
root.title("Intrusion Detection Alerts")

# Create a Text widget
text_widget = tk.Text(root, wrap='word', height=20, width=50)
text_widget.pack(expand=True, fill='both')

# Redirect stdout to the Text widget
sys.stdout = RedirectOutput(text_widget)

# Start the alert generation thread
start_alerts_thread()

# Run the Tkinter main loop
root.mainloop()
