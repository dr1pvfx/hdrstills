# PQ Image Converter

A simple GUI application for converting images with PQ (Perceptual Quantizer) color space using ImageMagick.

## Prerequisites

Before building the application, you need to have the following installed:

1. Python 3.8 or higher
2. ImageMagick (install using Homebrew: `brew install imagemagick`)
3. pip (Python package manager)

## Building the Application

1. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Build the application:
   ```bash
   pyinstaller --windowed --add-data "ITUR_2100_PQ_FULL.ICC:." pq_converter.py
   ```

3. The application will be created in the `dist` folder as `pq_converter.app`

## Usage

1. Double-click the `pq_converter.app` to launch the application
2. Click "Browse" to select an input TIFF file
3. The output path will be automatically set, but you can change it by clicking the output "Browse" button
4. Click "Convert" to process the image
5. The converted image will be saved with the specified output path

## Features

- Simple and intuitive GUI interface
- Support for TIFF input files
- Automatic output path suggestion
- Progress feedback and error handling
- Built-in ICC profile for PQ color space conversion 