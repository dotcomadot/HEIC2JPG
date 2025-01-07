# HEIC2JPG


HEIC to JPG Converter

This Python script converts HEIC images in a directory to JPG format. It uses multithreading for fast and efficient conversion, supports preserving EXIF metadata, and allows customization of output quality.

Features

HEIC to JPG Conversion:

Converts HEIC images to JPG while preserving EXIF metadata and timestamps.

Parallel Processing:

Utilizes multithreading for faster conversion using the ThreadPoolExecutor.

User Interaction:

Prompts the user if the ConvertedFiles folder already exists.

Skips files that have already been converted.

Command-Line Interface:

Customize the input directory, JPG quality, and number of workers.

Progress Indicator:

Displays conversion progress dynamically in the terminal.



Usage

Save the Script:
Save the Python script as heic_to_jpg.py.

Run the Script:
Use the command line to execute the script with the required arguments.

Command-Line Arguments

heic_dir (required): The path to the directory containing HEIC images.

-q, --quality (optional): Output JPG quality (1-100). Default: 50.

-w, --workers (optional): Number of parallel threads for processing. Default: 4.

Example

python heic_to_jpg.py /path/to/heic/images -q 90 -w 8

