import os
import sys
from pathlib import Path

try:
    import PyPDF2
except ImportError:
    print("PyPDF2 is not installed. Installing...")
    os.system(f"{sys.executable} -m pip install PyPDF2")
    import PyPDF2

def convert_pdf_to_text(pdf_path, txt_path):
    """
    Convert a single PDF file to text file.
    
    Args:
        pdf_path (str): Path to the input PDF file
        txt_path (str): Path to the output text file
    """
    try:
        with open(pdf_path, 'rb') as pdf_file:
            # Create PDF reader object
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Extract text from all pages
            text_content = []
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                if text.strip():  # Only add non-empty pages
                    text_content.append(text)
            
            # Write extracted text to output file
            with open(txt_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write('\n\n'.join(text_content))
            
            return True
    except Exception as e:
        print(f"Error converting {pdf_path}: {str(e)}")
        return False

def sanitize_filename(filename):
    """
    Replace spaces with hyphens and remove other problematic characters.
    
    Args:
        filename (str): Original filename without extension
    
    Returns:
        str: Sanitized filename
    """
    # Replace spaces with hyphens
    filename = filename.replace(' ', '-')
    # Optional: Remove other problematic characters
    # Uncomment the following line if needed
    # filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    return filename

def convert_all_pdfs_in_folder(folder_path='.'):
    """
    Convert all PDF files in the specified folder to text files.
    
    Args:
        folder_path (str): Path to the folder containing PDF files
    """
    # Convert to Path object for easier handling
    folder = Path(folder_path)
    
    if not folder.exists():
        print(f"Error: Folder '{folder_path}' does not exist.")
        return
    
    if not folder.is_dir():
        print(f"Error: '{folder_path}' is not a directory.")
        return
    
    # Find all PDF files
    pdf_files = list(folder.glob('*.pdf')) + list(folder.glob('*.PDF'))
    
    if not pdf_files:
        print(f"No PDF files found in '{folder_path}'.")
        return
    
    print(f"Found {len(pdf_files)} PDF file(s) in '{folder_path}'")
    print("-" * 50)
    
    converted_count = 0
    failed_count = 0
    
    for pdf_path in pdf_files:
        # Get the filename without extension
        base_name = pdf_path.stem
        
        # Sanitize the filename (replace spaces with hyphens)
        sanitized_name = sanitize_filename(base_name)
        
        # Create output text file path
        txt_path = pdf_path.parent / f"{sanitized_name}.txt"
        
        # Convert PDF to text
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
    # Check if folder path is provided as command line argument
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
    else:
        # Default to current directory
        folder_path = '.'
    
    convert_all_pdfs_in_folder(folder_path)

if __name__ == "__main__":
    main()
