from fillpdf import fillpdfs as fp
from pypdf import PdfReader, PdfWriter
import os
import json

class Util:

  # NOTE - IMPORTANT: This function is used to get the values of the form field keys to be used in `field_keys` in dicts.py. To get these values fill out a sample 1095 form and run the following code providing the path to the filled out form
  @staticmethod
  def print_form_fields(file_path: str):
    """
    Prints the form fields of a PDF file.
    :param file_path: The path to the PDF file.
    """
    form_fields = fp.get_form_fields(file_path)
    json_str = json.dumps(form_fields, indent=2)
    print(json_str)

  @staticmethod
  def merge_pdfs(source_dir: str, output_file: str):
    """
    Merges all PDF files in the source directory into a single PDF file.
    :param source_dir: The directory containing the PDF files to merge.
    :param output_file: The path to the output file.
    """
    # Create a PdfWriter object for the output file
    writer = PdfWriter()

    # Loop through all the PDF files in the source directory
    for i, item in enumerate(sorted(os.listdir(source_dir))):
      if item.endswith('.pdf'):  # Check if the file is a PDF
        # Construct the full path to the file
        file_path = os.path.join(source_dir, item)
        
        # Create a PdfReader object for the current PDF
        reader = PdfReader(file_path)
        
        # Assuming each PDF has only one page, add the first page to the writer
        writer.add_page(reader.pages[0])

    # Write out the merged PDF to the output file
    with open(output_file, 'wb') as f_out:
      writer.write(f_out)

    print(f"All PDFs in '{source_dir}' have been merged into '{output_file}'")