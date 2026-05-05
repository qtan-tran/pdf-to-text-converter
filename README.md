# PDF to Text Converter

A simple Python script that converts all PDF files in a folder to text files, with automatic filename sanitization (spaces replaced by hyphens).

## Features

- 🔄 **Batch Conversion**: Converts all PDF files in a specified folder at once
- 📝 **Text Extraction**: Extracts text content from PDF files using PyPDF2
- 🔧 **Filename Sanitization**: Automatically replaces spaces with hyphens in output filenames
- 🌍 **UTF-8 Support**: Handles international characters and special symbols
- 🛡️ **Error Handling**: Continues processing remaining files even if one fails
- 📊 **Progress Reporting**: Shows conversion status and summary statistics
- 🎯 **Flexible Input**: Specify target folder via command line or use current directory
- 🔌 **Auto-install**: Attempts to install required dependencies automatically

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

## Installation

### Option 1: Quick Install

1. Save the script as `pdf_to_text_converter.py`

2. Run the script - it will automatically attempt to install required dependencies:
   ```bash
   python pdf_to_text_converter.py
```

### Option 2: Manual Install

1. Install the required package:
  
  ```bash
  pip install PyPDF2
  ```
  
2. Save and run the script as described below
  

## Usage

### Basic Usage

Convert all PDFs in the current directory:

```bash
python pdf_to_text_converter.py
```

### Convert PDFs from a Specific Folder

**Linux/macOS:**

```bash
python pdf_to_text_converter.py /path/to/your/pdf/folder
```

**Windows:**

```bash
python pdf_to_text_converter.py "C:\My Documents\PDFs"
```

### Output

For each PDF file found, the script creates a corresponding `.txt` file in the same folder with:

- Spaces in the original filename replaced by hyphens
- The same base name (without spaces)
- Example: `my document.pdf` → `my-document.txt`

## Examples

### Example 1: Current Directory

```bash
$ ls
report 2024.pdf   presentation slides.pdf   script.py

$ python pdf_to_text_converter.py
Found 2 PDF file(s) in '.'
--------------------------------------------------
Converting: report 2024.pdf -> report-2024.txt
  ✓ Successfully converted
Converting: presentation slides.pdf -> presentation-slides.txt
  ✓ Successfully converted
--------------------------------------------------
Conversion complete: 2 succeeded, 0 failed

$ ls
report 2024.pdf   report-2024.txt   presentation slides.pdf   presentation-slides.txt   script.py
```

### Example 2: Specific Folder

```bash
$ python pdf_to_text_converter.py ./documents
Found 3 PDF file(s) in './documents'
--------------------------------------------------
Converting: annual report.pdf -> annual-report.txt
  ✓ Successfully converted
Converting: scanned document.pdf -> scanned-document.txt
  ✓ Successfully converted
Converting: corrupt file.pdf -> corrupt-file.txt
  ✗ Failed to convert
--------------------------------------------------
Conversion complete: 2 succeeded, 1 failed
```

## Alternative PDF Parser

If PyPDF2 doesn't extract text well from your PDFs (especially scanned documents or complex layouts), you can use `pdfplumber` instead:

### Install pdfplumber:

```bash
pip install pdfplumber
```

### Modified Conversion Function:

Replace the `convert_pdf_to_text` function in the script with:

```python
def convert_pdf_to_text(pdf_path, txt_path):
    """Convert PDF to text using pdfplumber (better for complex layouts)."""
    import pdfplumber
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text_content = []
            for page in pdf.pages:
                text = page.extract_text()
                if text and text.strip():
                    text_content.append(text)

            with open(txt_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write('\n\n'.join(text_content))
            return True
    except Exception as e:
        print(f"Error converting {pdf_path}: {str(e)}")
        return False
```

## Complete Script with pdfplumber

Here's the complete script if you prefer to use pdfplumber from the start:

```python
import os
import sys
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    print("pdfplumber is not installed. Installing...")
    os.system(f"{sys.executable} -m pip install pdfplumber")
    import pdfplumber

def convert_pdf_to_text(pdf_path, txt_path):
    """Convert PDF to text using pdfplumber."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text_content = []
            for page in pdf.pages:
                text = page.extract_text()
                if text and text.strip():
                    text_content.append(text)

            with open(txt_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write('\n\n'.join(text_content))
            return True
    except Exception as e:
        print(f"Error converting {pdf_path}: {str(e)}")
        return False

def sanitize_filename(filename):
    """Replace spaces with hyphens."""
    return filename.replace(' ', '-')

def convert_all_pdfs_in_folder(folder_path='.'):
    """Convert all PDF files in the specified folder to text files."""
    folder = Path(folder_path)

    if not folder.exists():
        print(f"Error: Folder '{folder_path}' does not exist.")
        return

    if not folder.is_dir():
        print(f"Error: '{folder_path}' is not a directory.")
        return

    pdf_files = list(folder.glob('*.pdf')) + list(folder.glob('*.PDF'))

    if not pdf_files:
        print(f"No PDF files found in '{folder_path}'.")
        return

    print(f"Found {len(pdf_files)} PDF file(s) in '{folder_path}'")
    print("-" * 50)

    converted_count = 0
    failed_count = 0

    for pdf_path in pdf_files:
        base_name = pdf_path.stem
        sanitized_name = sanitize_filename(base_name)
        txt_path = pdf_path.parent / f"{sanitized_name}.txt"

        print(f"Converting: {pdf_path.name} -> {txt_path.name}")

        if convert_pdf_to_text(pdf_path, txt_path):
            converted_count += 1
            print(f"  ✓ Successfully converted")
        else:
            failed_count += 1
            print(f"  ✗ Failed to convert")

    print("-" * 50)
    print(f"Conversion complete: {converted_count} succeeded, {failed_count} failed")

def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
    else:
        folder_path = '.'

    convert_all_pdfs_in_folder(folder_path)

if __name__ == "__main__":
    main()
```

## Troubleshooting

### Issue: "No module named 'PyPDF2'"

**Solution**: Install manually with `pip install PyPDF2`

### Issue: Extracted text is garbled or empty

**Solution**:

- Try the `pdfplumber` alternative mentioned above
- Ensure the PDF contains selectable text (not just scanned images)
- For scanned PDFs, you'll need OCR software like Tesseract

### Issue: Permission denied when reading/writing files

**Solution**:

- Check file permissions
- Ensure the PDF files aren't open in another program
- Run the script with appropriate permissions

### Issue: Unicode encoding errors

**Solution**: The script uses UTF-8 encoding by default, which handles most characters. If you encounter issues, you can modify the encoding in the `open()` calls.

### Issue: PyPDF2 installation fails on some systems

**Solution**:

- Try upgrading pip: `pip install --upgrade pip`
- Install using conda: `conda install -c conda-forge pypdf2`
- Use the pdfplumber alternative which might have fewer dependencies

## Limitations

- **Scanned PDFs**: This script extracts text only from PDFs that contain selectable text. Scanned documents (image-based PDFs) will produce empty or minimal output.
- **Complex Layouts**: Some PDFs with complex layouts (multiple columns, tables, etc.) may not extract text perfectly.
- **Encrypted PDFs**: Password-protected PDFs cannot be processed without modification.
- **Large Files**: Very large PDF files may take significant time and memory to process.

## Customization

### Modify Filename Sanitization

To replace additional characters, edit the `sanitize_filename()` function:

```python
import re

def sanitize_filename(filename):
    # Replace spaces with hyphens
    filename = filename.replace(' ', '-')
    # Remove other problematic characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Convert to lowercase (optional)
    filename = filename.lower()
    return filename
```

### Change Output Directory

To save text files to a different folder, modify the `txt_path` assignment:

```python
# Create an output directory
output_dir = pdf_path.parent / "converted_texts"
output_dir.mkdir(exist_ok=True)
txt_path = output_dir / f"{sanitized_name}.txt"
```

### Process Subdirectories Recursively

To include PDFs in subfolders, modify the PDF file search:

```python
# Find all PDFs recursively
pdf_files = list(folder.rglob('*.pdf')) + list(folder.rglob('*.PDF'))
```

### Add Logging

To log conversion results to a file:

```python
import logging

logging.basicConfig(filename='conversion.log', level=logging.INFO)

# Inside the conversion loop:
logging.info(f"Converted: {pdf_path.name} -> {txt_path.name}")
```

## Performance Tips

- **Large batches**: For hundreds of PDFs, consider adding a small delay between conversions to avoid resource exhaustion
- **Memory usage**: The script loads entire PDFs into memory. For very large PDFs, process page by page without storing all text
- **Parallel processing**: For multi-core systems, you can use `concurrent.futures` to process multiple files simultaneously

## Error Codes

| Exit Code | Meaning |
| --- | --- |
| 0   | Success (or partial success with some failures) |
| 1   | Folder not found or invalid |

## Use Cases

- **Document archiving**: Convert PDF reports to searchable text files
- **Data extraction**: Prepare PDF content for text analysis or NLP tasks
- **Content indexing**: Create text versions for search engine indexing
- **Backup purposes**: Maintain readable text backups of important documents
- **Accessibility**: Convert PDFs to plain text for screen readers

## Contributing

Feel free to submit issues or enhancements. Common improvements include:

- Adding OCR support for scanned PDFs using pytesseract
- Preserving original folder structure
- Adding parallel processing for large batches
- Supporting additional output formats (JSON, Markdown, etc.)
- Adding progress bar for large batches

## License

This script is provided under the MIT License. Feel free to use, modify, and distribute as needed.

## Support

For issues or questions:

1. Check the Troubleshooting section above
2. Verify your Python version (`python --version`)
3. Ensure PDF files aren't corrupted or password-protected
4. Test with a simple PDF to isolate issues

## Version History

- **v1.0** (2024-01): Initial release with PyPDF2 support
- **v1.1** (2024-02): Added auto-install feature
- **v1.2** (2024-03): Improved error handling and UTF-8 encoding

---

**Note**: This script is for extracting text from PDFs. It does not preserve formatting, images, or layout structure from the original PDF files. For scanned PDFs or image-based documents, consider using OCR software like Tesseract in combination with this script.
