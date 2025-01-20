imageInfo
imageInfo is a Python-based GUI application designed to extract and display metadata and GPS location (if available) from image files (JPEG, PNG). It also provides functionality to open the location in Google Maps, copy the URL to the clipboard, and save metadata to a text file.

Features
Metadata Extraction
EXIF Metadata: View detailed EXIF metadata from image files.

GPS Location: Extract GPS coordinates (latitude and longitude) from images.

Google Maps Integration: Open the extracted location in Google Maps directly from the application.

Copy URL: Copy the Google Maps URL to the clipboard.

Save Metadata: Save metadata and GPS information to a text file.

Thumbnail Preview: Display a thumbnail of the selected image.

User Interface
Simple and Intuitive: Easy-to-use interface for viewing metadata and GPS information.

Real-Time Updates: Automatically refresh metadata and location information when a new image is loaded.

Installation
Prerequisites
To run imageInfo, ensure the following tools are installed on your system:

Python 3.x: The script is written in Python 3.

Pillow: For image processing and metadata extraction.

Tkinter: For the graphical user interface (usually included with Python).

Pyperclip: For copying text to the clipboard.

Step-by-Step Installation
1. Install Required Dependencies
Install the required Python libraries using pip:

bash
Copy
pip install pillow pyperclip
2. Clone the Repository
Clone the repository to your local machine:

bash
Copy
git clone https://github.com/ALSRKAL/imageInfo.git
cd imageInfo
3. Run the Application
Start the application:

bash
Copy
python image_info.py
Usage
Loading an Image
Launch the application.

Click Open Image to select an image file (JPEG or PNG).

View the metadata and GPS location (if available) in the respective textboxes.

Google Maps Integration
If GPS data is available, click Open in Google Maps to view the location on Google Maps.

Use the Copy URL button to copy the Google Maps URL to the clipboard.

Saving Metadata
Click Save Metadata to save the metadata and GPS information to a text file.

Screenshots
Main Interface
Main Interface

Contributing
Contributions are welcome! If you'd like to contribute, please follow these steps:

Fork the repository.

Create a new branch for your feature or bugfix.

Commit your changes.

Submit a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments
Inspired by various image metadata extraction tools.

Thanks to the open-source community for providing the libraries used in this project.

Contact
For questions or feedback, feel free to reach out:

GitHub: ALSRKAL

Email: mohammedalsrkal@gmail.com

Enjoy using imageInfo! 🚀

Notes:
