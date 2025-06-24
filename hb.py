import os  # Import the os module for file and directory operations
import sys  # Import the sys module for command-line arguments and exiting
import re  # Import the re module for regular expressions


def clean_filename(filename):
    """Remove problematic punctuation from filename, keeping hyphens, parentheses and file extension"""
    # Split filename and extension
    name, ext = os.path.splitext(filename)

    # Keep only alphanumeric characters, hyphens, underscores, spaces, and parentheses
    # Remove problematic characters like: : * ? " < > | / \ etc.
    cleaned_name = re.sub(r"[^\w\s\-\(\)]", "", name)

    # Replace multiple spaces with single space and strip
    cleaned_name = re.sub(r"\s+", " ", cleaned_name).strip()

    return cleaned_name + ext  # Return the cleaned filename with its extension


if len(sys.argv) != 2:  # Check if exactly one argument (the directory) is provided
    print("Usage: python hb.py <directory>")  # Print usage message
    sys.exit(1)  # Exit with error code

directory = sys.argv[1]  # Get the directory path from command-line argument

if not os.path.isdir(directory):  # Check if the provided path is a valid directory
    print(f"Error: '{directory}' is not a valid directory")  # Print error message
    sys.exit(1)  # Exit with error code

# Create 'done' subdirectory if it doesn't exist
done_dir = os.path.join(directory, "done")  # Path for the 'done' subdirectory
os.makedirs(done_dir, exist_ok=True)  # Create the 'done' directory if it doesn't exist

print(f"Scanning directory: {directory}")  # Print scanning message
all_files = os.listdir(directory)  # List all files and directories in the given directory
mkv_files = []  # Initialize a list to store MKV filenames

for filename in all_files:  # Iterate over all files/directories in the directory
    filepath = os.path.join(directory, filename)  # Get the full path of the file
    if os.path.isfile(filepath):  # Check if it's a file (not a directory)
        print(f"\nFound file: ")  # Print found file message
        if filename.lower().endswith(".mkv"):  # Check if the file is an MKV file
            # Check if filename needs cleaning
            cleaned_filename = clean_filename(filename)

            if cleaned_filename != filename:  # If the cleaned filename is different
                print(f"  🔧 Renaming: {filename} -> {cleaned_filename}")  # Print renaming message
                cleaned_filepath = os.path.join(directory, cleaned_filename)  # Path for the cleaned filename

                # Rename the file if the new name doesn't already exist
                if not os.path.exists(cleaned_filepath):  # Check if cleaned filename doesn't exist
                    os.rename(filepath, cleaned_filepath)  # Rename the file
                    mkv_files.append(cleaned_filename)  # Add cleaned filename to MKV list
                    print(f"  ✅ MKV file renamed and detected: {cleaned_filename}")  # Print success message
                else:
                    print(f"  ⚠️  Cannot rename: {cleaned_filename} already exists")  # Print warning
                    mkv_files.append(filename)  # Add original filename to MKV list
                    print(f"  ✅ MKV file detected (not renamed): {filename}")  # Print detection message
            else:
                mkv_files.append(filename)  # Add filename to MKV list
                print(f"  ✅ MKV file detected: {filename}")  # Print detection message
        else:
            print(f"  ❌ Not MKV: {filename}")  # Print not MKV message

print(f"\nTotal files found: {len(all_files)}")  # Print total files found
print(f"MKV files to process: {len(mkv_files)}")  # Print number of MKV files to process
# breakpoint = input("\nPress Enter to continue or Ctrl+C to exit...")  # (Commented out) Pause for user input

for filename in mkv_files:  # Iterate over MKV files
    filepath = os.path.join(directory, filename)  # Get full path of the MKV file
    # Create output path in the 'done' subdirectory
    base_name, _ = os.path.splitext(filename)  # Split filename and extension
    output_filepath = os.path.join(done_dir, f"{base_name}.mp4")  # Output path for the converted file
    print(f"\nProcessing file: {filepath}")  # Print processing message
    print(f"Output will be: {output_filepath}\n")  # Print output file path
    os.system(
        f"flatpak run --command=HandBrakeCLI fr.handbrake.ghb -i '{filepath}' -o '{output_filepath}' --preset='General/Super HQ 1080p30 Surround'"
    )  # Run HandBrakeCLI to convert MKV to MP4
print("\n✅ Processing complete.")  # Print completion message
os.system(f"systemctl suspend")  # Suspend the system after processing
