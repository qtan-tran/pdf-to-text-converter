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
