import PyPDF2
from PIL import Image
from pptx import Presentation
from docx import Document
from zipfile import BadZipFile
from docx.opc.exceptions import PackageNotFoundError
from pptx.exc import PackageNotFoundError
from openpyxl import load_workbook

def is_pdf_encrypted(filepath):
    try:
        with open(filepath, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(filepath)
            if pdf_reader.is_encrypted:
                return 1  # Password encryption
            else:
                return 0  # Regular PDF
    except Exception as e:
        return 2  # Malicious encryption

def check_image_metadata(image_path):
    try:
        with Image.open(image_path) as img:
            metadata = img.info
            return metadata
    except Exception as e:
        return None

def is_pptx_encrypted(file_path):
    try:
        pres = Presentation(file_path)
        # Attempt to access metadata
        metadata = pres.core_properties
        # If metadata is retrievable, file is likely not encrypted
        return False
    except (PackageNotFoundError, BadZipFile):
        # If an exception is raised, the file might be encrypted or corrupted
        return True

def is_docx_encrypted(file_path):
    try:
        doc = Document(file_path)
        # Attempt to access metadata
        metadata = doc.core_properties
        # If metadata is retrievable, file is likely not encrypted
        return False
    except Exception as e:
        # If an exception is raised, the file might be encrypted or corrupted
        return True
    
def is_xlsx_encrypted(file_path):
    try:
        # Load the workbook and access properties
        wb = load_workbook(file_path)
        # Check the metadata
        metadata = wb.properties
           
        return False
        
    except Exception as e:
        
        return True