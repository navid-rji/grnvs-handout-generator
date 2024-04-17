import PyPDF2
import re
import argparse

def process_pdf(input_pdf_path, output_pdf_path):
    reader = PyPDF2.PdfFileReader(input_pdf_path)
    writer = PyPDF2.PdfFileWriter()

    first_page = reader.pages[0]
    writer.add_page(first_page)

    page_number_dict = {}

    for i in range(1, len(reader.pages)):
        page = reader.pages[i]
        text = page.extract_text()
        page_number = parse_page_number(text)

        if page_number is not None:
            page_number_dict[page_number] = page

    for page_number in sorted(page_number_dict.keys()):
        writer.add_page(page_number_dict[page_number])

    with open(output_pdf_path, 'wb') as f:
        writer.write(f)

def parse_page_number(text):
    match = re.search(r'Kapitel.*?(\d+-\d+)$', text)
    if match:
        return int(match.group().split('-')[-1])
    return None

def main():
    parser = argparse.ArgumentParser(description="Process GRNVS slides to create a handout.")
    parser.add_argument('input_pdf_path', type=str, help="The path to the input PDF file")
    parser.add_argument('output_pdf_path', type=str, help="The path to the output PDF file")
    args = parser.parse_args()
    process_pdf(args.input_pdf_path, args.output_pdf_path)

if __name__ == '__main__':
    main()