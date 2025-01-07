import os
import logging
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from tkinter import Tk, filedialog, Label, Button, IntVar, Scale
from tkinter.messagebox import showinfo, showerror
from PIL import Image, UnidentifiedImageError
from pillow_heif import register_heif_opener

logging.basicConfig(level=logging.INFO, format='%(message)s')


def convert_single_file(heic_path, jpg_path, output_quality) -> tuple:
    try:
        with Image.open(heic_path) as image:
            exif_data = image.info.get("exif")
            image.save(jpg_path, "JPEG", quality=output_quality, exif=exif_data)
            heic_stat = os.stat(heic_path)
            os.utime(jpg_path, (heic_stat.st_atime, heic_stat.st_mtime))
            return heic_path, True
    except (UnidentifiedImageError, FileNotFoundError, OSError) as e:
        logging.error("Error converting '%s': %s", heic_path, e)
        return heic_path, False


def convert_heic_to_jpg_ui(heic_dir, output_quality=50, max_workers=4):
    register_heif_opener()

    if not os.path.isdir(heic_dir):
        showerror("Error", f"Directory '{heic_dir}' does not exist.")
        return

    jpg_dir = os.path.join(heic_dir, "ConvertedFiles")
    if os.path.exists(jpg_dir):
        response = filedialog.askyesno(
            "Existing Folder", 
            "Existing 'ConvertedFiles' folder detected. Delete and proceed?"
        )
        if not response:
            return
        shutil.rmtree(jpg_dir)
    os.makedirs(jpg_dir, exist_ok=True)

    heic_files = [file for file in os.listdir(heic_dir) if file.lower().endswith(".heic")]
    total_files = len(heic_files)

    if total_files == 0:
        showinfo("No Files", "No HEIC files found in the directory.")
        return

    tasks = []
    for file_name in heic_files:
        heic_path = os.path.join(heic_dir, file_name)
        jpg_path = os.path.join(jpg_dir, os.path.splitext(file_name)[0] + ".jpg")

        if os.path.exists(jpg_path):
            continue

        tasks.append((heic_path, jpg_path))

    num_converted = 0
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {
            executor.submit(convert_single_file, heic_path, jpg_path, output_quality): heic_path
            for heic_path, jpg_path in tasks
        }

        for future in as_completed(future_to_file):
            _, success = future.result()
            if success:
                num_converted += 1

    showinfo("Conversion Completed", f"Successfully converted {num_converted} files.")


def select_directory():
    directory = filedialog.askdirectory(title="Select HEIC Directory")
    if directory:
        dir_label.config(text=f"Selected Directory: {directory}")
        start_button.config(state="normal")
        start_button.directory = directory


def start_conversion():
    directory = start_button.directory
    quality = quality_scale.get()
    convert_heic_to_jpg_ui(directory, output_quality=quality)


# GUI Setup
root = Tk()
root.title("HEIC to JPG Converter")

dir_label = Label(root, text="Select a directory containing HEIC files:")
dir_label.pack(pady=10)

select_button = Button(root, text="Browse", command=select_directory)
select_button.pack(pady=5)

quality_label = Label(root, text="Select Output Quality:")
quality_label.pack(pady=10)

quality_scale = Scale(root, from_=1, to=100, orient="horizontal", length=300)
quality_scale.set(50)
quality_scale.pack(pady=5)

start_button = Button(root, text="Start Conversion", state="disabled", command=start_conversion)
start_button.pack(pady=20)

root.mainloop()
