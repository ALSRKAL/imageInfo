from PIL import Image, ImageTk
from PIL.ExifTags import TAGS, GPSTAGS
import webbrowser
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import pyperclip  # For copying text to clipboard

def get_image_metadata(image_path):
    """
    Extracts metadata from an image using Pillow.
    """
    try:
        # Open the image using Pillow
        image = Image.open(image_path)
        # Extract metadata
        metadata = image._getexif()
        if metadata:
            metadata_text = "Image Metadata:\n"
            for tag_id, value in metadata.items():
                tag_name = TAGS.get(tag_id, tag_id)
                metadata_text += f"{tag_name}: {value}\n"
            return metadata_text
        else:
            return "No metadata found in the image."
    except Exception as e:
        return f"Error reading metadata: {e}"

def get_decimal_from_dms(dms, ref):
    """
    Convert degrees, minutes, seconds (DMS) to decimal degrees.
    """
    degrees = dms[0]
    minutes = dms[1] / 60.0
    seconds = dms[2] / 3600.0

    decimal = degrees + minutes + seconds

    if ref in ['S', 'W']:
        decimal = -decimal

    return decimal

def get_image_location(image_path):
    """
    Extracts GPS location (latitude and longitude) from an image if available.
    """
    try:
        # Open the image using Pillow
        image = Image.open(image_path)
        # Extract metadata
        metadata = image._getexif()
        if metadata:
            # Extract GPSInfo
            gps_info = metadata.get(34853, {})  # 34853 is the tag ID for GPSInfo
            if gps_info:
                gps_text = "\nGPS Info:\n"
                for key, value in gps_info.items():
                    tag_name = GPSTAGS.get(key, key)
                    gps_text += f"{tag_name}: {value}\n"

                # Extract latitude and longitude
                lat = gps_info.get(2, None)
                lat_ref = gps_info.get(1, None)
                lon = gps_info.get(4, None)
                lon_ref = gps_info.get(3, None)

                if lat and lon and lat_ref and lon_ref:
                    # Convert latitude and longitude to decimal degrees
                    lat_decimal = get_decimal_from_dms(lat, lat_ref)
                    lon_decimal = get_decimal_from_dms(lon, lon_ref)

                    location_text = f"\nImage Location (GPS):\nLatitude: {lat_decimal}, Longitude: {lon_decimal}"
                    gps_text += location_text

                    # Return GPS text and Google Maps URL
                    google_maps_url = f"https://www.google.com/maps?q={lat_decimal},{lon_decimal}"
                    gps_text += f"\n\nGoogle Maps URL: {google_maps_url}"
                    return gps_text, google_maps_url
                else:
                    return "\nIncomplete GPS data found in the image.", None
            else:
                return "\nNo GPS data found in the image.", None
        else:
            return "\nNo metadata found in the image.", None
    except Exception as e:
        return f"Error reading EXIF data: {e}", None

def open_image():
    """
    Open a file dialog to select an image and display its metadata and location.
    """
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
    )
    if file_path:
        load_image(file_path)

def load_image(file_path):
    """
    Load an image and display its metadata, location, and thumbnail.
    """
    # Update status bar
    status_var.set("Loading image...")
    root.update_idletasks()

    # Display metadata
    metadata_text = get_image_metadata(file_path)
    metadata_textbox.delete(1.0, tk.END)  # Clear previous text
    metadata_textbox.insert(tk.END, metadata_text)

    # Display GPS location (if available)
    location_text, google_maps_url = get_image_location(file_path)
    location_textbox.delete(1.0, tk.END)  # Clear previous text
    location_textbox.insert(tk.END, location_text)

    # Enable/disable the "Open in Google Maps" and "Copy URL" buttons
    if google_maps_url:
        open_maps_button.config(state=tk.NORMAL)
        copy_url_button.config(state=tk.NORMAL)
        global current_url
        current_url = google_maps_url
    else:
        open_maps_button.config(state=tk.DISABLED)
        copy_url_button.config(state=tk.DISABLED)

    # Display thumbnail
    try:
        image = Image.open(file_path)
        image.thumbnail((200, 200))  # Resize image to fit in the thumbnail area
        photo = ImageTk.PhotoImage(image)
        thumbnail_label.config(image=photo)
        thumbnail_label.image = photo  # Keep a reference to avoid garbage collection
    except Exception as e:
        thumbnail_label.config(image=None)
        messagebox.showerror("Error", f"Failed to load thumbnail: {e}")

    # Update status bar
    status_var.set("Ready")

def clear_textboxes():
    """
    Clear the metadata and location textboxes.
    """
    metadata_textbox.delete(1.0, tk.END)
    location_textbox.delete(1.0, tk.END)
    open_maps_button.config(state=tk.DISABLED)
    copy_url_button.config(state=tk.DISABLED)
    thumbnail_label.config(image=None)
    status_var.set("Ready")

def open_in_google_maps():
    """
    Open the Google Maps URL in the default web browser.
    """
    if current_url:
        webbrowser.open(current_url)

def copy_url_to_clipboard():
    """
    Copy the Google Maps URL to the clipboard.
    """
    if current_url:
        pyperclip.copy(current_url)
        messagebox.showinfo("Copied", "Google Maps URL copied to clipboard!")

def save_metadata_to_file():
    """
    Save the metadata and GPS location to a text file.
    """
    metadata = metadata_textbox.get(1.0, tk.END)
    location = location_textbox.get(1.0, tk.END)
    if metadata.strip() or location.strip():
        file_path = filedialog.asksaveasfilename(
            title="Save Metadata",
            filetypes=[("Text Files", "*.txt")],
            defaultextension=".txt"
        )
        if file_path:
            with open(file_path, "w") as file:
                file.write("Metadata:\n")
                file.write(metadata)
                file.write("\nGPS Location:\n")
                file.write(location)
            messagebox.showinfo("Saved", "Metadata saved successfully!")
    else:
        messagebox.showwarning("No Data", "No metadata or GPS location to save.")

def toggle_dark_mode():
    """
    Toggle between dark and light mode.
    """
    if dark_mode.get():
        root.tk_setPalette(background="#2d2d2d", foreground="#ffffff")
        metadata_textbox.config(bg="#2d2d2d", fg="#ffffff")
        location_textbox.config(bg="#2d2d2d", fg="#ffffff")
    else:
        root.tk_setPalette(background="#ffffff", foreground="#000000")
        metadata_textbox.config(bg="#ffffff", fg="#000000")
        location_textbox.config(bg="#ffffff", fg="#000000")

# Create the main window
root = tk.Tk()
root.title("Image Metadata and Location Viewer")
root.geometry("800x700")

# Use ttk for a modern look
style = ttk.Style()
style.theme_use("clam")

# Create a frame for buttons
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

# Create a button to open an image
open_button = ttk.Button(button_frame, text="Open Image", command=open_image)
open_button.grid(row=0, column=0, padx=5)

# Create a button to clear textboxes
clear_button = ttk.Button(button_frame, text="Clear", command=clear_textboxes)
clear_button.grid(row=0, column=1, padx=5)

# Create a button to open Google Maps
open_maps_button = ttk.Button(button_frame, text="Open in Google Maps", command=open_in_google_maps, state=tk.DISABLED)
open_maps_button.grid(row=0, column=2, padx=5)

# Create a button to copy Google Maps URL
copy_url_button = ttk.Button(button_frame, text="Copy URL", command=copy_url_to_clipboard, state=tk.DISABLED)
copy_url_button.grid(row=0, column=3, padx=5)

# Create a button to save metadata to file
save_button = ttk.Button(button_frame, text="Save Metadata", command=save_metadata_to_file)
save_button.grid(row=0, column=4, padx=5)

# Create a frame for metadata and location
info_frame = ttk.Frame(root)
info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

# Create a textbox to display metadata
metadata_label = ttk.Label(info_frame, text="Metadata:")
metadata_label.pack()
metadata_textbox = scrolledtext.ScrolledText(info_frame, width=100, height=15)
metadata_textbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

# Create a textbox to display GPS location
location_label = ttk.Label(info_frame, text="GPS Location:")
location_label.pack()
location_textbox = scrolledtext.ScrolledText(info_frame, width=100, height=10)
location_textbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

# Create a frame for the thumbnail
thumbnail_frame = ttk.Frame(root)
thumbnail_frame.pack(fill=tk.X, padx=10, pady=10)

# Create a label to display the thumbnail
thumbnail_label = ttk.Label(thumbnail_frame)
thumbnail_label.pack()

# Create a status bar
status_var = tk.StringVar()
status_var.set("Ready")
status_bar = ttk.Label(root, textvariable=status_var, relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# Variable to store the current Google Maps URL
current_url = None

# Dark mode toggle
dark_mode = tk.BooleanVar()
dark_mode_button = ttk.Checkbutton(root, text="Dark Mode", variable=dark_mode, command=toggle_dark_mode)
dark_mode_button.pack(side=tk.RIGHT, padx=10, pady=10)

# Run the application
root.mainloop()