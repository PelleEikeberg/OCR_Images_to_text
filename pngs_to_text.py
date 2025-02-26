#!/usr/bin/env python3

import argparse
import os
import sys
import subprocess
import shutil
import platform
import time

def get_next_output_filename(output_dir: str) -> str:
    """
    Returns the first available 'output.txt' or 'output_N.txt' file name
    in output_dir, so we don't overwrite an existing file.
    """
    base_name = "output"
    extension = ".txt"
    candidate = os.path.join(output_dir, base_name + extension)
    counter = 0
    while os.path.exists(candidate):
        counter += 1
        candidate = os.path.join(output_dir, f"{base_name}_{counter}{extension}")
    return candidate

def main():
    # If no arguments are provided, show a friendly help message and exit.
    if len(sys.argv) == 1:
        print("""
Welcome to the Screenshot Text Extractor!

This tool extracts text from PNG image files (screenshots) found in a folder
and combines the extracted text into a single file. It uses a built-in text
recognition engine if one is not already installed on your system.

USAGE:
    python images_to_text.py <folder_of_images> [optional_output_filename] [OPTIONS]

OPTIONS:
    --language LANG    : Specify the language for text extraction, e.g., 'eng' for English or 'nor' for Norwegian (default: eng).
    --tesseract-cmd CMD: Specify the command or path for the text recognition engine.
                         If not provided, the tool will try to use the built-in version if necessary.

EXAMPLES:
    1) python images_to_text.py my_images_folder
       (Processes all PNG files in 'my_images_folder' and writes the combined text to a new file.)

    2) python images_to_text.py my_images_folder combined_output.txt
       (Uses a specific output file name.)

    3) python images_to_text.py my_images_folder --language nor
       (Uses Norwegian for text extraction.)

Please re-run with the required arguments.
""")
        sys.exit(0)

    # Set up argument parsing.
    parser = argparse.ArgumentParser(
        description="Extract text from PNG screenshots and combine the results into one text file."
    )
    parser.add_argument(
        "input_folder",
        help="Path to the folder containing PNG image files."
    )
    parser.add_argument(
        "output_file",
        nargs="?",
        default=None,
        help="Optional name for the combined output text file. If omitted, a new file is created automatically."
    )
    parser.add_argument(
        "--language", "-l",
        default="eng",
        choices=["eng", "nor", "deu", "fra", "spa"],
        help="Language code for text extraction (default: eng)."
    )
    parser.add_argument(
        "--tesseract-cmd",
        default="tesseract",
        help="Command or path for the text recognition engine (default: tesseract)."
    )

    args = parser.parse_args()

    # Determine directories.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_folder = os.path.abspath(args.input_folder)
    output_dir = os.path.join(script_dir, "extracted_text")
    os.makedirs(output_dir, exist_ok=True)

    # Record any .txt files already present in the output folder.
    preexisting_txt_files = {f for f in os.listdir(output_dir) if f.lower().endswith('.txt')}

    # Determine final output file path.
    if args.output_file is None:
        combined_output_path = get_next_output_filename(output_dir)
    else:
        output_file = args.output_file if args.output_file.lower().endswith(".txt") else args.output_file + ".txt"
        combined_output_path = os.path.join(output_dir, output_file)

    if not os.path.isdir(input_folder):
        print(f"ERROR: '{input_folder}' is not a valid directory.")
        sys.exit(1)

    all_files = os.listdir(input_folder)
    image_files = [f for f in all_files if f.lower().endswith(".png")]

    if not image_files:
        print(f"No PNG files found in '{input_folder}'. Nothing to process.")
        sys.exit(0)

    # Check if the text recognition engine is available.
    if not shutil.which(args.tesseract_cmd):
        # Try to use the built-in version from the companion "Tesseract-OCR" folder.
        tesseract_exec = "tesseract.exe" if os.name == "nt" else "tesseract"
        companion_path = os.path.join(script_dir, "Tesseract-OCR", tesseract_exec)
        if os.path.exists(companion_path):
            args.tesseract_cmd = companion_path
        else:
            print("ERROR: Text recognition engine not found. Please install Tesseract or place it in the 'Tesseract-OCR' folder.")
            sys.exit(1)

    print(f"Found {len(image_files)} PNG file(s) in '{input_folder}'. Beginning text extraction using language '{args.language}'...")
    generated_text_files = []
    num_files = len(image_files)

    # Process each image file with the text recognition engine.
    for idx, image_file in enumerate(image_files):
        image_path = os.path.join(input_folder, image_file)
        base_name = os.path.splitext(image_file)[0]
        temp_output_path = os.path.join(output_dir, base_name + ".txt")

        try:
            subprocess.run(
                [
                    args.tesseract_cmd,
                    image_path,
                    os.path.splitext(temp_output_path)[0],
                    "-l", args.language
                ],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            generated_text_files.append(temp_output_path)
        except subprocess.CalledProcessError as e:
            print(f"\nERROR: Text extraction failed for {image_file}.\n{e}")

        # Update a simple progress bar.
        progress = (idx + 1) / num_files
        filled = int(progress * 10)
        bar = "(" + "=" * filled + " " * (10 - filled) + ")"
        sys.stdout.write(f"\rProcessing files: {bar} {int(progress*100)}% complete")
        sys.stdout.flush()
        time.sleep(0.1)  # Small pause for visual effect

    print("\n\nCombining extracted text into:", combined_output_path)
    with open(combined_output_path, 'w', encoding='utf-8') as combined:
        for txt_path in generated_text_files:
            if os.path.exists(txt_path):
                with open(txt_path, 'r', encoding='utf-8') as infile:
                    combined.write(infile.read())
                    combined.write("\n")

    print("\nSummary:")
    print(f" - Input folder: {input_folder}")
    print(f" - Number of images processed: {len(image_files)}")
    print(f" - Combined output file: {combined_output_path}")

    print("\nFirst 10 lines of the combined output:")
    try:
        with open(combined_output_path, 'r', encoding='utf-8') as combined:
            for i in range(10):
                line = combined.readline()
                if not line:
                    break
                print(line.rstrip())
    except FileNotFoundError:
        print("[No output file found. Something may have gone wrong.]")

    # Delete the temporary .txt files created during this run,
    # but keep any .txt files that were already present.
    for txt_path in generated_text_files:
        if os.path.exists(txt_path) and os.path.basename(txt_path) not in preexisting_txt_files:
            os.remove(txt_path)

    print("\nDone.")

if __name__ == "__main__":
    main()
