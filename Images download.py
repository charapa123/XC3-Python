import requests
import os
from urllib.parse import urlparse, quote
import pandas as pd

# Load data from CSV into a DataFrame
df = pd.read_csv(r'C:\Users\Charlie Pavlou\Documents\Python inputs\Hero Info images.csv')

# Specify the directory where you want to save the images
image_directory = "Hero Info images"

# Create the directory if it doesn't exist
os.makedirs(image_directory, exist_ok=True)

# Loop through the DataFrame rows and download images
for index, row in df.iterrows():
    colony, image_url, region = row

    # Parse the URL to get the filename without the /show
    parsed_url = urlparse(image_url)
    filename = os.path.basename(parsed_url.path.split('/show')[0])
    
    # Encode the URL to replace invalid characters
    encoded_url = quote(image_url, safe='')

    # Combine the initial part of the URL with the extracted filename
    filepath = os.path.join(image_directory, filename)
    
    # Send a GET request to download the image
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded image for {colony} as {filename}")
    else:
        print(f"Failed to download image for {colony}")


