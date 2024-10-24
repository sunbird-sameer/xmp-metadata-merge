import os
import subprocess

# Function to run the exiftool command for merging metadata from .xmp to image/video
def merge_metadata(image_path, xmp_path):
    try:
        # Run exiftool to merge metadata from .xmp to the image/video file
        result = subprocess.run(['exiftool', '-overwrite_original', '-tagsfromfile', xmp_path, image_path], check=True)
        print(f"Metadata merged for {image_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to merge metadata for {image_path}: {e}")
        return False

# Function to delete .xmp file if the metadata is merged successfully
def delete_xmp_file(xmp_path):
    try:
        os.remove(xmp_path)
        print(f"Deleted .xmp file: {xmp_path}")
    except OSError as e:
        print(f"Error deleting file {xmp_path}: {e}")

# Function to find images/videos and corresponding .xmp files
def process_directory_and_cleanup(root_folder):
    for subdir, dirs, files in os.walk(root_folder):
        for file in files:
            file_path = os.path.join(subdir, file)
            
            # Check if the file is an image or video (you can expand this list based on your file types)
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.mp4', '.mov', '.avi')):
                # Look for the corresponding .xmp file
                xmp_file = file_path + '.xmp'  # Assuming .xmp has the same base name
                
                if os.path.exists(xmp_file):
                    # If .xmp file exists, attempt to merge the metadata
                    if merge_metadata(file_path, xmp_file):
                        # If merge was successful, delete the .xmp file
                        delete_xmp_file(xmp_file)
                else:
                    print(f"No .xmp file found for {file_path}")

# Set the root folder where your images/videos and .xmp files are stored
root_folder = 'path/to/folder/with/photos/and/xmp/files/'  # Update this path to your folder location

# Start processing the directory and cleaning up .xmp files
process_directory_and_cleanup(root_folder)
