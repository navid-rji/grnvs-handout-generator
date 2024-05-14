import fitz
import re
import argparse

def process_pdf(input_pdf_path, output_pdf_path):
    doc = fitz.open(input_pdf_path)
    out = fitz.open()

    page_number_dict = {}

    print("Scanning pages for page numbers...")
    next_page_number = 0
    for i, page in enumerate(doc):
        text = page.get_text()
        page_number = parse_page_number(text)
        if page_number is not None:
            page_number_dict[page_number] = i
            next_page_number = page_number + 1
        else:
            page_number_dict[next_page_number] = i
            next_page_number += 1

        if i < doc.page_count - 1:
            print(f"{progress_bar(i+1, doc.page_count)} {i+1}/{doc.page_count}", end='\r')
        else:
            print(f"{progress_bar(i+1, doc.page_count)} {i+1}/{doc.page_count}")

    print("Creating handout...")
    final_num_of_pages = len(page_number_dict)
    for i, page_number in enumerate(sorted(page_number_dict.keys())):
        out.insert_pdf(doc, from_page=page_number_dict[page_number], to_page=page_number_dict[page_number])
        if i < final_num_of_pages - 1:
            print(f"{progress_bar(i+1, final_num_of_pages)} {i+1}/{final_num_of_pages}", end='\r')
        else:
            print(f"{progress_bar(i+1, final_num_of_pages)} {i+1}/{final_num_of_pages}")

    print("Writing handout to file...")
    out.save(output_pdf_path)
    out.close()
    doc.close()
    print("Done!")

def parse_page_number(text):
    match = re.search(r'Kapitel.*?(\d+-\d+)', text, re.DOTALL)
    if match:
        return int(match.group().split('-')[-1])
    return None

def progress_bar(progress, total):
    bar_length = 50
    progress = int(progress * bar_length / total)
    return f"[{'=' * progress}{' ' * (bar_length - progress)}]"

def main():
    parser = argparse.ArgumentParser(description="Process GRNVS slides to create a handout.")
    parser.add_argument('input_pdf_path', type=str, help="The path to the input PDF file")
    parser.add_argument('output_pdf_path', type=str, help="The path to the output PDF file")
    args = parser.parse_args()
    process_pdf(args.input_pdf_path, args.output_pdf_path)

if __name__ == '__main__':
    main()