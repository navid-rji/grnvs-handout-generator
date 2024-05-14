# GRNVS Slide Handout Creator
This Python script generates handouts from GRNVS (Grundlagen: Rechnernetze und Verteilte Systeme) course slides by condensing multiple slides for the same page number into just the last slide of each number. This simplifies the material for easier study.

## Requirements
- Python 3.x
- PyMuPDF library

## Installation
Install the PyPDF2 package using pip:

```bash
pip3 install PyMuPDF
```

## Usage
Run the script with the paths to the input and output PDF files:

```bash
python3 grnvsHandout.py <input_pdf_path> <output_pdf_path>
```

## Example
To process slides.pdf and output the handout to handout.pdf:

```bash
python3 grnvsHandout.py slides.pdf handout.pdf
```
