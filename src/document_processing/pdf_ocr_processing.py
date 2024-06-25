import mimetypes
import os
from pathlib import Path
import argparse

import dotenv

from google.api_core.client_options import ClientOptions
from google.cloud import documentai
from google.cloud.documentai_v1 import Document

import PyPDF2

# Load Env Files.
# This will return RuntimeError if your env vars are not loaded successfully
if not dotenv.load_dotenv():
    raise RuntimeError("Failed to load .env file")

class DocumentAI:
    """Wrapper class around GCP's DocumentAI API."""
    def __init__(self) -> None:

        self.client_options = ClientOptions(  # type: ignore
            api_endpoint=f"{os.getenv('GCP_REGION')}-documentai.googleapis.com",
            credentials_file=os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
        )
        self.client = documentai.DocumentProcessorServiceClient(client_options=self.client_options)
        self.processor_name = self.client.processor_path(
            os.getenv("GCP_PROJECT_ID"),
            os.getenv("GCP_REGION"),
            os.getenv("GCP_PROCESSOR_ID")
        )

    def __call__(self, file_path: Path) -> Document:
        """Convert a local PDF into a GCP document. Performs full OCR extraction and layout parsing."""

        # Read the file into memory
        with open(file_path, "rb") as file:
            content = file.read()

        mime_type = mimetypes.guess_type(file_path)[0]
        raw_document = documentai.RawDocument(content=content, mime_type=mime_type)

        # Configure the process request
        request = documentai.ProcessRequest(
            name=self.processor_name,
            raw_document=raw_document
        )

        result = self.client.process_document(request=request)
        document = result.document

        return document

def split_pdf(input_pdf:str, pages_per_split: int, temp_folder:str) -> None:

    # Create the temp folder if it doesn't exist
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)
    else:
        # Empty the temp folder if it already exists
        files = os.listdir(temp_folder)
        # Iterate over the files and delete each file
        for file_name in files:
            file_path = Path(temp_folder) / file_name
            os.remove(file_path)

    # Open the input PDF
    with open(input_pdf, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        total_pages = len(reader.pages)
        
        # Determine the number of output files
        num_splits = (total_pages // pages_per_split) + (1 if total_pages % pages_per_split else 0)
        
        for i in range(num_splits):
            # Create a PDF writer object
            writer = PyPDF2.PdfWriter()
            
            # Calculate the start and end pages for this split
            start_page = i * pages_per_split
            end_page = min(start_page + pages_per_split, total_pages)
            
            # Add the specified pages to the writer
            for page_num in range(start_page, end_page):
                writer.add_page(reader.pages[page_num])
            
            # Write the split PDF to a new file
            output_filename = f"split_{i + 1}.pdf"

            # Write the file to the temp folder
            with open(f'temp/{output_filename}', "wb") as output_file:
                writer.write(output_file)
            
            # print(f"Created: {output_filename}")

def run(input_pdf: str) -> None:
    pdf_content = ''
    temp_folder = 'temp'
    output_file_name = "pdf_content.txt"
    document_ai = DocumentAI()

    # split_pdf('data/inpatient_record.pdf', 15)
    split_pdf(input_pdf, 15, temp_folder)

    # Get a list of all files in the temp folder
    files = os.listdir(temp_folder)
    sorted_files = sorted(files, key=lambda x: int(x.split('_')[1].split('.')[0]))

    # Iterate over the files and call the document_ai function for each file
    for file_name in sorted_files:
        file_path = Path(temp_folder) / file_name
        document = document_ai(file_path)
        pdf_content += document.text
        
    output_file_path = Path(temp_folder) / output_file_name

    with open(output_file_path, "w") as file:
        file.write(pdf_content)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--path-to-case-pdf',
                        metavar='path',
                        type=str,
                        required=True,
                        help='Path to local test case with which to run your code')
    args = parser.parse_args()
    input_pdf = args.path_to_case_pdf
    run(input_pdf)