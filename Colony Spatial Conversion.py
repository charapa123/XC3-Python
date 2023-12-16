import csv
import pyproj
import pandas as pd
import os

# Define the projection system for your data with the updated parameters
custom_projection = pyproj.Proj(
    proj="lcc",
    lat_1=33,
    lat_2=45,
    lon_0=-95,
    x_0=0,
    y_0=0,
    a=6378137,
    b=6356752.314,
    units="m",
    datum="WGS84",
)

# Directory containing input files (CSV format)
input_directory = r"C:\Users\Charlie Pavlou\Documents\Python inputs\Colonies"

# Output file name for latitude and longitude results (CSV format)
output_file = "coordinates_with_latlon_Colonies.csv"

# Create an output file for latitude and longitude results
with open(output_file, mode="w", newline="") as output_csv:
    fieldnames = ["Latitude", "Longitude", "Region"]
    writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
    writer.writeheader()

    # Define the maximum X and Y coordinates of your image
    max_x = 2500
    max_y = 2500

    # Process each input file in the directory
    for filename in os.listdir(input_directory):
        if filename.endswith(".csv"):  # Ensure it's a CSV file
            input_file_path = os.path.join(input_directory, filename)

            # Extract the region name from the filename (remove the ".csv" extension)
            region = os.path.splitext(filename)[0]

            # Open the input file for reading (CSV format)
            with open(input_file_path, mode="r", newline="") as input_csv:
                reader = csv.reader(input_csv)
                for row in reader:
                    # Assuming the first and second columns are X and Y (adjust indices if needed)
                    x = float(row[0])
                    y = float(row[1])

                    # Adjust the X and Y values to the new maximum coordinates (2500,2500)
                    adjusted_x = (x / 2500) * max_x
                    adjusted_y = (y / 2500) * max_y

                    # Convert (adjusted_x, adjusted_y) to (longitude, latitude)
                    longitude, latitude = custom_projection(adjusted_x, adjusted_y, inverse=True)

                    # Write the results to the output file
                    writer.writerow({
                        "Latitude": latitude,
                        "Longitude": longitude,
                        "Region": region
                    })

print(f"Conversion complete. Results saved to {output_file}")



