import PyPDF2
import re
import argparse

def process_pdf(input_pdf_path, output_pdf_path):
    reader = PyPDF2.PdfReader(input_pdf_path)
    writer = PyPDF2.PdfWriter()

    first_page = reader.pages[0]
    writer.add_page(first_page)

    page_number_dict = {}

    print("Scanning pages for page numbers...")

    for i in range(1, len(reader.pages)):
        page = reader.pages[i]
        text = page.extract_text()
        page_number = parse_page_number(text)

        if page_number is not None:
            page_number_dict[page_number] = page    

        if i < len(reader.pages) - 1:
            print(f"{progress_bar(i, len(reader.pages))} {i}/{len(reader.pages)}", end='\r')
        else:
            print(f"{progress_bar(i, len(reader.pages))} {i}/{len(reader.pages)}")

    print("Creating handout...")
    final_num_of_pages = len(page_number_dict)
    pages_added = 0
    for page_number in sorted(page_number_dict.keys()):

        writer.add_page(page_number_dict[page_number])
        pages_added += 1
        if pages_added < final_num_of_pages:
            print(f"{progress_bar(pages_added, final_num_of_pages)} {pages_added}/{final_num_of_pages}", end='\r')
        else:
            print(f"{progress_bar(pages_added, final_num_of_pages)} {pages_added}/{final_num_of_pages}")

    print("Writing handout to file...")

    with open(output_pdf_path, 'wb') as f:
        writer.write(f)

    print("Done!")

def parse_page_number(text):
    match = re.search(r'(\d+)$', text)
    if match:
        return int(match.group())
    return None

def progress_bar(progress, total):
    bar_length = 50
    progress = int(progress * bar_length / total)
    return f"[{'=' * progress}{' ' * (bar_length - progress)}]"

def main():
    parser = argparse.ArgumentParser(description="Process Theo slides to create a handout.")
    parser.add_argument('input_pdf_path', type=str, help="The path to the input PDF file")
    parser.add_argument('output_pdf_path', type=str, help="The path to the output PDF file")
    args = parser.parse_args()
    process_pdf(args.input_pdf_path, args.output_pdf_path)

if __name__ == '__main__':
    main()