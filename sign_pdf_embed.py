from PyPDF2 import PdfFileReader, PdfFileWriter
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.backends import default_backend

def load_private_key_from_pkcs12(p12_file_path, password=None):
    with open(p12_file_path, "rb") as p12_file:
        private_key, certificate, additional_certs = pkcs12.load_key_and_certificates(
            p12_file.read(), password.encode() if password else None, backend=default_backend()
        )
        return private_key, certificate

def sign_pdf(input_pdf_path, output_pdf_path, pkcs12_path, pkcs12_password):
    # Read the input PDF
    with open(input_pdf_path, 'rb') as input_pdf_file:
        reader = PdfFileReader(input_pdf_file)
        writer = PdfFileWriter()
        for page_num in range(reader.getNumPages()):
            writer.addPage(reader.getPage(page_num))

    # Load the PKCS#12 certificate
    private_key, certificate = load_private_key_from_pkcs12(pkcs12_path, pkcs12_password)
    
    # Add the signature to the PDF (simple text, not a cryptographic signature)
    writer.addMetadata({
        '/Title': 'Signed PDF',
        '/Author': 'Your Name',
        '/Subject': 'Signed using a digital certificate',
        '/Keywords': 'signed, digital signature'
    })

    with open(output_pdf_path, 'wb') as output_pdf_file:
        writer.write(output_pdf_file)
        
    # Note: Proper digital signing of PDFs usually involves cryptographic operations and would need a dedicated library for signing

if __name__ == "__main__":
    input_pdf_path = "input.pdf"
    output_pdf_path = "signed_output.pdf"
    pkcs12_path = "certificate.p12"
    pkcs12_password = "password"

    sign_pdf(input_pdf_path, output_pdf_path, pkcs12_path, pkcs12_password)
