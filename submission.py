import argparse

from document_processing import extract_structured_data, pdf_ocr_processing

def main(input_pdf:str) -> None:
    
    print(f"Running OCR processing with input PDF: {input_pdf}")
    pdf_ocr_processing.run(input_pdf)

    print(f"OCR processing completed. Running structured data extraction...")
    extract_structured_data.run()
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path-to-case-pdf',
                        metavar='path',
                        type=str,
                        required=True,
                        help='Path to local test case with which to run your code')
    args = parser.parse_args()
    input_pdf = args.path_to_case_pdf
    main(input_pdf)
