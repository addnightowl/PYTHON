'''
This is a simple desktop application that allows you to upload files to an S3 bucket.
'''

# Importing necessary modules for the GUI, file dialog, AWS connection, and other utilities.
import tkinter as tk
# Importing the file dialog module from tkinter.
from tkinter import filedialog
# Importing the customtkinter module for the custom toggle switch.
import customtkinter as ctk
# Importing the boto3 library for interacting with AWS services.
import boto3
# Importing the NoCredentialsError and PartialCredentialsError exceptions from the botocore library.
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
# Importing the os module to work with the operating system.
import os
# Importing the load_dotenv function from the dotenv library.
from dotenv import load_dotenv
# Importing the Image and ImageTk modules from the PIL library.
from PIL import Image, ImageTk
# Importing the pathlib module to work with file paths.
import pathlib
# Importing the requests module to make HTTP requests.
import requests
# Importing the BytesIO module from the io library to work with bytes for images.
from io import BytesIO

'''
You will  need to create a .env file in the root directory of the project and add the following environment variables:
# Full path to the .env file that contains the AWS credentials.
AWS_ENV_PATH="/full/path/to/.env"

# AWS Access Key ID.
AWS_ACCESS_KEY="Access Key ID for the IAM User"

# AWS Secret Access Key.
AWS_SECRET_KEY="Secret Access Key for the IAM User"

# AWS Region.
AWS_REGION="us-east-1"
'''
# Load the environment variables for AWS credentials from the specified path.
load_dotenv(os.environ.get("AWS_ENV_PATH"))

# Setting up AWS credentials to access S3.
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.environ.get("AWS_REGION")

# List of allowed extensions for images.
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Dictionary for non-image file icons
FILE_ICONS = {
    'pdf': 'https://add_image_url_here.png',
    'txt': 'https://add_image_url_here.png',
    'md': 'https://add_image_url_here.png',
    'json': 'https://add_image_url_here.png',
    'yaml': 'https://add_image_url_here.png',
    'doc': 'https://add_image_url_here.png',
    'docx': 'https://add_image_url_here.png',
    'js': 'https://add_image_url_here.png',
    'html': 'https://add_image_url_here.png',
    'css': 'https://add_image_url_here.png',
    'py': 'https://add_image_url_here.png',
    'others': 'https://add_image_url_here.png',
    # ... add other file types and their icon paths as needed
}

# Initialize the S3 client with the provided credentials and region.
s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)

# Function to show a preview of the selected file in the GUI.
def show_preview(file_path):
    file_extension = pathlib.Path(file_path).suffix[1:].lower()
    
    # Check if the file is an allowed image
    if file_extension in ALLOWED_EXTENSIONS:
        image = Image.open(file_path)
        image.thumbnail((100, 100))
        photo = ImageTk.PhotoImage(image)
        preview_label.config(image=photo)
        preview_label.image = photo
    # If the file is a known non-image type, show its icon
    elif file_extension in FILE_ICONS:
        icon_url = FILE_ICONS[file_extension]
        response = requests.get(icon_url)
        icon = Image.open(BytesIO(response.content))
        icon.thumbnail((100, 100))
        icon_photo = ImageTk.PhotoImage(icon)
        preview_label.config(image=icon_photo)
        preview_label.image = icon_photo
    # If the file type is unknown, just show a default icon
    else:
        icon_url = FILE_ICONS['others']  # Assuming you have an 'others' key for default icon
        response = requests.get(icon_url)
        icon = Image.open(BytesIO(response.content))
        icon.thumbnail((100, 100))
        icon_photo = ImageTk.PhotoImage(icon)
        preview_label.config(image=icon_photo)
        preview_label.image = icon_photo


# Function to upload a file to the specified S3 bucket.
def upload_file(file_path, bucket_name, folder_name):
    file_name = os.path.basename(file_path)
    if folder_name:
        file_name = f'{folder_name}/{file_name}'
    
    try:
        # Upload the file to the specified bucket.
        s3.upload_file(file_path, bucket_name, file_name)
        # Show a success message in the GUI.
        upload_message = f'Successfully uploaded to {bucket_name}/{file_name}'
        message_label.config(text=upload_message, fg="green")
    except (NoCredentialsError, PartialCredentialsError):
        # If there's an issue with AWS credentials, show an error message in the GUI.
        message_label.config(text='No credentials found.', fg="red")
    except Exception as e:
        # If any other error occurs, display it in the GUI.
        message_label.config(text=f'An error occurred: {e}', fg="red")

# Callback function to enable or disable the upload_button based on the bucket_name_entry content.
def on_entry_change(*args):
    # Check if the bucket_name_entry is empty.
    if bucket_name_var.get():
        upload_button.config(state=tk.NORMAL)
        # folder_checkbox.config(state=tk.NORMAL)
        folder_switch.configure(state=tk.NORMAL)
    # If the bucket_name_entry is empty, disable the create_button and folder_checkbox.
    else:
        upload_button.config(state=tk.DISABLED)
        # folder_checkbox.config(state=tk.DISABLED)
        folder_switch.configure(state=tk.DISABLED)

# Function to refresh the GUI.
def refresh_gui():
    # Resetting the preview label.
    preview_label.config(image=None)
    # Resetting the image in the preview label.
    preview_label.image=None
    # Resetting the message label.
    message_label.config(text="")
        
# Function to open file dialog and get the selected file path.
def open_file_dialog():
    # Refresh the GUI each time a new file dialog is opened.
    refresh_gui()
    file_path = filedialog.askopenfilename()
    bucket_name = bucket_name_entry.get()
    folder_name = folder_entry.get()
    
    if file_path and bucket_name:
        # Show a preview of the selected file in the GUI.
        show_preview(file_path)
        # Upload the file to the specified bucket and or bucket/folder.
        upload_file(file_path, bucket_name, folder_name)

# Function to toggle the folder entry field based on the toggle switch.
def toggle_folder_checkbox():
    # if folder_checkbox_var.get():
    if folder_swtich_var.get():
        folder_entry.config(state=tk.NORMAL)
    else:
        folder_entry.config(state=tk.DISABLED)
    
# Creating the main GUI window.
root = tk.Tk()
# Setting the title of the GUI window.
root.title("S3 Bucket Upload App")
# Setting the size of the GUI window.
root.geometry("500x475")

# Creating and placing the 'Bucket Name' label and entry field on the GUI.
bucket_label = tk.Label(root, text="Bucket Name (Required):", relief="groove")
# Placing the Bucket Name Label on the GUI.
bucket_label.pack(pady=5)
# Using a StringVar to monitor changes in the entry widget
bucket_name_var = tk.StringVar()
# Setting the initial value of the StringVar to an empty string
bucket_name_var.trace_add("write", on_entry_change)
# Creating the Bucket Name Entry field on the GUI.
bucket_name_entry = tk.Entry(root, textvariable=bucket_name_var, relief="sunken")
# Placing the Bucket Name Entry field on the GUI.
bucket_name_entry.pack(pady=5)

# Creating and placing the 'Folder Name' label and entry field on the GUI.
folder_label = tk.Label(root, text="Folder Name (Optional):", relief="groove")
# Placing the Folder Name Label on the GUI.
folder_label.pack(pady=5)
# Creating the Folder Name Entry field on the GUI.
folder_entry = tk.Entry(root, relief="sunken", state=tk.DISABLED)
# Placing the Folder Name Entry field on the GUI.
folder_entry.pack(pady=5)
# Using a StringVar to monitor changes in the entry widget.
folder_swtich_var = tk.IntVar()
# Creating the Toggle Switch to confirm adding a folder name.
folder_switch = ctk.CTkSwitch(root, text="Toggle to input existing folder name or\n input a new name to create a new folder!", variable=folder_swtich_var, command=toggle_folder_checkbox, state=ctk.DISABLED)
# Placing the Toggle Switch on the GUI.
folder_switch.pack(pady=5)

# Creating a frame for the image preview within the main GUI window
# Setting the width and height to match the thumbnail size
preview_frame = tk.Frame(root, bd=2, relief="sunken", width=100, height=100)
# Placing the preview frame in the GUI.
preview_frame.pack(pady=10, padx=10)
# Ensure the frame doesn't shrink. If you want it to expand to fit the image, you can omit this.
preview_frame.pack_propagate(False)
# Creating and placing the label to display the image preview on the GUI.
preview_label = tk.Label(preview_frame)
# Placing the image preview label in the frame.
preview_label.pack(pady=10)

# Creating a frame for the message label within the main GUI window
message_frame = tk.Frame(root, bd=2, relief="sunken")
# Placing the message frame in the GUI.
message_frame.pack(pady=10, padx=10, fill="x")
# Creating and placing the message label to display messages on the GUI.
message_label = tk.Label(message_frame, text="", wraplength=350)
# Placing the message label in the frame.
message_label.pack(pady=5)

# Creating and placing the 'Upload File' button on the GUI.
upload_button = tk.Button(root, text="Upload File", relief="raised", command=open_file_dialog, state=tk.DISABLED, foreground="green")  # Initially disabled
# Placing the Upload File Button on the GUI.
upload_button.pack(pady=10)

# Start the Tkinter event loop to run the GUI.
root.mainloop()
