# bulk_cli_mkv_util

A simple Python script to automatically clean MKV filenames and batch compress video files using HandBrake CLI via the command line.

## Overview

This utility helps automate the process of preparing and converting MKV video files by:
1. **Cleaning filenames** - Removes problematic punctuation that can cause issues with file systems while preserving hyphens and parentheses
2. **Batch processing** - Converts all MKV files in a directory using HandBrake CLI
3. **Organized output** - Places converted files in a "done" subdirectory for easy organization

## Features

- ✅ **Filename sanitization**: Removes problematic characters (`:`, `*`, `?`, `"`, `<`, `>`, `|`, `/`, `\`, etc.)
- ✅ **Preserves important characters**: Keeps hyphens (`-`) and parentheses (`()`) in filenames
- ✅ **Batch conversion**: Processes all MKV files in a directory automatically
- ✅ **Organized output**: Creates a "done" folder for converted MP4 files
- ✅ **Safety checks**: Prevents overwriting existing files during renaming
- ✅ **Detailed logging**: Shows progress and actions taken for each file
- ✅ **User confirmation**: Pause before processing to review what will be converted

## Requirements

- Python 3.x
- HandBrake CLI installed via Flatpak
- Linux system with bash shell

### Installing HandBrake CLI

```bash
flatpak install flathub fr.handbrake.ghb
```

## Usage

```bash
python hb.py <directory_path>
```

### Example

```bash
python hb.py /path/to/your/videos
```

## How It Works

1. **Scans the directory** for all files
2. **Identifies MKV files** (case-insensitive)
3. **Cleans filenames** by removing problematic punctuation:
   - `Movie: The Beginning (2023).mkv` → `Movie The Beginning (2023).mkv`
   - `Action*Movie?.mkv` → `ActionMovie.mkv`
   - `TV-Show (S01E01).mkv` → `TV-Show (S01E01).mkv` (unchanged)
4. **Renames files** if needed (with conflict checking)
5. **Shows summary** of files to be processed
6. **Waits for user confirmation** before starting conversion
7. **Converts each MKV** to MP4 using HandBrake's "Super HQ 1080p30 Surround" preset
8. **Saves output** to `done/` subdirectory

## File Structure After Processing

```
your_video_directory/
├── original_file1.mkv
├── original_file2.mkv
└── done/
    ├── original_file1.mkv.mp4
    └── original_file2.mkv.mp4
```

## HandBrake Settings

The script uses HandBrake's built-in preset:
- **Preset**: `General/Super HQ 1080p30 Surround`
- **Output format**: MP4
- **Quality**: High quality 1080p at 30fps with surround sound

## Error Handling

- Validates that the provided directory exists
- Checks for file conflicts before renaming
- Skips non-MKV files automatically
- Provides clear error messages and usage instructions

## Example Output

```
Scanning directory: /home/user/videos
Found file: Movie- The Best Film (2023).mkv
  🔧 Renaming: Movie- The Best Film (2023).mkv -> Movie The Best Film (2023).mkv
  ✅ MKV file renamed and detected: Movie The Best Film (2023).mkv
Found file: Another Movie.mkv
  ✅ MKV file detected: Another Movie.mkv
Found file: document.txt
  ❌ Not MKV: document.txt

Total files found: 3
MKV files to process: 2
['Movie The Best Film (2023).mkv', 'Another Movie.mkv']

Press Enter to continue or Ctrl+C to exit...
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.
