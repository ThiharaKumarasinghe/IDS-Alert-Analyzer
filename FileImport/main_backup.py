import customtkinter as ctk # type: ignore
from fileImport_functions import select_file, save_file, upload_pcap_file
from PIL import Image, ImageTk # PIL -> Python Image Library



# Create the main application window
root = ctk.CTk()
root.title("IDS Alert Analyser")
root.geometry("1000x750")
root.resizable(False, False)

# Appearance mode
# ctk.set_appearance_mode("system")  # default
# ctk.set_appearance_mode("dark")
ctk.set_appearance_mode("light")

# Configure the grid layout for the root
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

# Load the background image
background_image = Image.open("FileImport/background_fileImport.png")  # Read the background image
background_image = background_image.resize((500, 750))  # Resize the image to fit
background_image = background_image.transpose(Image.FLIP_LEFT_RIGHT)  # Flip the image horizontally (left to right)
background_photo = ImageTk.PhotoImage(background_image)
# background_image.show()


# Create a frame for the left side (background and project name)
left_frame = ctk.CTkFrame(root, width=500, height=750, corner_radius=0)
left_frame.grid(row=0, column=0, sticky="nswe")


# Add the background image
bg_label = ctk.CTkLabel(left_frame, image=background_photo, text="")
bg_label.place(x=0, y=0, relwidth=1, relheight=1)


# # Add the project name over the background image
# project_name_label = ctk.CTkLabel(left_frame, text="IDS Alert Analyser", 
#                                   font=("Montserrat Black", 36, "bold"), 
#                                   text_color="white", fg_color="transparent", 
#                                   padx=20, pady=5)
# project_name_label.place(relx=0.5, rely=0.3, anchor="center")

# # Add the project description with text wrapping
# project_description_label = ctk.CTkLabel(left_frame, 
#                                          text=("This tool allows you to upload and analyze your PCAP (Packet Capture) files. "
#                                                "Using advanced processing techniques, it will provide detailed insights and explanations "
#                                                "of the network traffic captured in your files."), 
#                                          text_color="white", 
#                                          wraplength=350,  # Set wrap length to fit within the frame
#                                          font=("Montserrat", 14))
# project_description_label.place(relx=0.5, rely=0.6, anchor="center")

# Right Frame for other widgets------------------------------------------------------------------------------------------
right_frame = ctk.CTkFrame(root, corner_radius=0)
right_frame.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

# Configure grid for right_frame to center widgets
right_frame.grid_columnconfigure(0, weight=1)
right_frame.grid_rowconfigure([1, 2, 3, 4, 5, 6], weight=0)
right_frame.grid_rowconfigure([0, 7], weight=1)

# Welcome back Label
welcome_label = ctk.CTkLabel(right_frame, text="Welcome back!", font=("Montserrat Black", 24, "bold"))
welcome_label.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

# IDS Alert Analyser Label
project_name_right_label = ctk.CTkLabel(right_frame, text="IDS Alert Analyser", font=("Montserrat Black", 36))
project_name_right_label.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)

# Description Label
description_label = ctk.CTkLabel(right_frame, 
                                 text=("This tool allows you to upload and analyze your PCAP (Packet Capture) files. "
                                       "Using advanced processing techniques, it will provide detailed insights and explanations "
                                       "of the network traffic captured in your files."),
                                 wraplength=350, font=("Montserrat", 14))
description_label.grid(row=3, column=0, sticky="nsew", padx=10, pady=5)

# Bold Call-to-Action Label
cta_label = ctk.CTkLabel(right_frame, 
                         text=("Get started by uploading a PCAP file"
                               " to see the analysis results."),
                         wraplength=350,
                         font=("Montserrat Bold", 16, "bold"))
cta_label.grid(row=4, column=0, sticky="nsew", padx=10, pady=10)



# Upload Button
upload_button = ctk.CTkButton(right_frame, text="Upload PCAP File", command=upload_pcap_file)
upload_button.grid(row=5, column=0, sticky="nsew", padx=10, pady=20)

# Start the main loop of the application
root.mainloop()