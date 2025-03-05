# OCR_Images_to_text
A simple Python script that uses Tesseract OCR to go through images (.png) and turn them into a single .txt file. Perfect for LLM (AI) usage

### Requirements:
This Python script will require you to have Tesseract installed
(main github page)
https://github.com/tesseract-ocr/tesseract

If you can run tesseract from the terminal running `tesseract,` you should be good as the rest of the code uses default Python packages. 

You may also place the Tesseract files in the "Tesseract-OCR" helper folder instead of adding them to the PATH environment (for Windows).

## Usage:

Running `pngs_to_text.py` directly will give a short guide, however, the usage is (*note: that "python" is optional as the file has a bang to use python when program is not specified*):
```
python images_to_text.py <folder_of_images> [optional_output_filename] [OPTIONS]
```
The most common option to use would be:

* to modify the language used by the `-l` or `--language`. (default is English "eng")
* `optional_output_filename` replacing it with a fitting name (e.g, paper_i_scanned.txt), where the default will be `output.txt`

The `input_folder` is non optional, and assumes a content of only `*.png` files which is named in correct order (as often is the case with default screenshots names).
