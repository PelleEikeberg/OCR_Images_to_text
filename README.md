# OCR_Images_to_text
A Simple python script which uses Tesseract OCR to go trough images (.png) and turn them into a single .txt file. Perfect of LLM (AI) usage

### Requirements:
This python script will require you have tesseract installed
(main github page)
https://github.com/tesseract-ocr/tesseract

If you can run tesseract from the terminal running `tesseract` you should be good as the rest if default python packages. 

If you wish to place the tesseract files in the "Tesseract-OCR" helper folder instead of adding to the PATH enviroment (for Windows) you may do so also.

## Usage:

Running `pngs_to_text.py` directly will give a short guide, however the usage is (*note: that "python" is option as the file has a bang to use python when program is not specified*):
```
python images_to_text.py <folder_of_images> [optional_output_filename] [OPTIONS]
```
Where the most common option to use would be:

* to modify the language used by the `-l` or `--language`. (default is english "eng")
* `optional_output_filename` replacing it with a fitting name (e.g paper_i_scanned.txt), where the default will be `output.txt`

The `input_folder` is non optional, and assumes a content of only `*.png` files which is named in correct order (as often is the case with default screenshots names).
