import os
import requests
from PIL import Image
from io import BytesIO

def download_image(url, filename):
    """Download an image from URL and save it to disk."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        img = Image.open(BytesIO(response.content))
        
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Save the image
        img.save(filename)
        print(f"Successfully downloaded {filename}")
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def download_crime_reporting_images():
    """Download all required images for the crime reporting application."""
    # Create images directory if it doesn't exist
    if not os.path.exists('images'):
        os.makedirs('images')
    
    # Define image URLs to download (replace with actual URLs)
    images = {
        'police_background.jpg': 'https://source.unsplash.com/L4YGuSg0fxs/1600x900',  # Police badge/car background
        'crime_scene.jpg': 'https://source.unsplash.com/Nyvq2juw4_o/800x500',         # Crime scene tape
        'police_station.jpg': 'https://source.unsplash.com/VBe9zj-JHW4/800x500',       # Police station/officer
        'emergency.jpg': 'https://source.unsplash.com/YOZ1ZB9s4DQ/800x500',           # Emergency response vehicle
        'cyber_crime.jpg': 'https://source.unsplash.com/DnDaQ-XCl4E/800x500',         # Computer/cybercrime themed
        'police_logo.png': 'https://source.unsplash.com/eeSdJfLfx1A/200x200'          # Police logo/badge
    }
    
    # Download each image
    for filename, url in images.items():
        filepath = os.path.join('images', filename)
        download_image(url, filepath)
    
    print("Image download completed.")

if __name__ == "__main__":
    download_crime_reporting_images()