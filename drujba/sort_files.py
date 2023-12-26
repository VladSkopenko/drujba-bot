import os
import shutil

# List of folders and their corresponding extensions
folders = ['images', 'videos', 'documents', 'music', 'archives']
extensions = {
    'images': ('.jpeg', '.png', '.jpg', '.svg'),
    'videos': ('.avi', '.mp4', '.mov', '.mkv'),
    'documents': ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'),
    'music': ('.mp3', '.ogg', '.wav', '.amr'),
    'archives': ('.zip', '.gz', '.tar'),
}


def find_files(path):
    # Recursively find all files in the given path
    path_to_files = []
    for file in os.listdir(path):
        new_path = os.path.join(path, file)
        if os.path.isdir(new_path):
            path_to_files.extend(find_files(new_path))
        else:
            path_to_files.append(new_path)
    return path_to_files


def sort_by_type(path):
    path = path.strip()  # Clean the path from leading and trailing spaces
    unknown_dir = os.path.join(path, 'unknown')

    # Create the 'unknown' directory if it doesn't exist
    if not os.path.exists(unknown_dir):
        os.makedirs(unknown_dir)

    # Create destination directories for each file type
    for folder in folders:
        destination_dir = os.path.join(path, folder)
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

    files = find_files(path)

    for file in files:
        name, extension = os.path.splitext(file)
        extension = extension.lower()

        # Move the file to the corresponding directory based on its extension
        moved = False
        for folder_name in folders:
            if extension in extensions[folder_name]:
                dest_file_path = os.path.join(path, folder_name, os.path.basename(file))
                if os.path.exists(dest_file_path):
                    base, ext = os.path.splitext(os.path.basename(file))
                    count = 1
                    while os.path.exists(os.path.join(path, folder_name, f"{base}_{count}{ext}")):
                        count += 1
                    dest_file_path = os.path.join(path, folder_name, f"{base}_{count}{ext}")
                shutil.move(file, dest_file_path)
                moved = True
                break

        # If the file doesn't match any known extension, move it to the 'unknown' directory
        if not moved:
            dest_file_path = os.path.join(unknown_dir, os.path.basename(file))
            if os.path.exists(dest_file_path):
                base, ext = os.path.splitext(os.path.basename(file))
                count = 1
                while os.path.exists(os.path.join(unknown_dir, f"{base}_{count}{ext}")):
                    count += 1
                dest_file_path = os.path.join(unknown_dir, f"{base}_{count}{ext}")
            shutil.move(file, dest_file_path)

    # Print the list of files in each category
    for folder_name in folders:
        print(f"List of {folder_name}:", os.listdir(os.path.join(path, folder_name)))

    # Print the list of files with unknown extensions
    print("List of files with unknown extensions:", os.listdir(unknown_dir))


