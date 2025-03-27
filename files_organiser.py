import os
import shutil

# Define the dictionary for file type categories
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"],
    "Videos": [".mp4", ".mkv", ".flv", ".avi", ".mov"],
    "PDFs": [".pdf"],  # Separate category for PDFs
    "Word Documents": [".doc", ".docx"],  # Separate category for Word files
    "Text Files": [".txt"],
    "PowerPoint Presentations": [".ppt", ".pptx"],
    "Excel Sheets": [".xls", ".xlsx"],
    "Audio": [".mp3", ".wav", ".aac", ".flac"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Data": [".csv", ".json", ".xml"],
    "Others": []
}

def organize_files(directory):
    """Organizes files in the given directory by their file types."""
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory.")
        return

    # Create folders for each category if not exist
    for category in FILE_CATEGORIES:
        folder_path = os.path.join(directory, category)
        os.makedirs(folder_path, exist_ok=True)

    # Move files into appropriate folders
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        # Skip directories
        if os.path.isdir(file_path):
            continue

        # Check file extension and move to corresponding folder
        file_moved = False
        for category, extensions in FILE_CATEGORIES.items():
            if any(filename.lower().endswith(ext) for ext in extensions):
                shutil.move(file_path, os.path.join(directory, category, filename))
                file_moved = True
                break

        # Move to "Others" if no match
        if not file_moved:
            shutil.move(file_path, os.path.join(directory, "Others", filename))

    print(f"Files in '{directory}' have been organized successfully!")

# Example usage
directory_to_organize = input("Enter the directory path to organize: ")
organize_files(directory_to_organize)
