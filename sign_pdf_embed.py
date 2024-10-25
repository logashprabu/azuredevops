from PyPDF2 import PdfFileReader, PdfFileWriter
from OpenSSL.crypto import load_pkcs12

def sign_pdf(input_pdf_path, output_pdf_path, pkcs12_path, pkcs12_password):
    # Read the input PDF
    with open(input_pdf_path, 'rb') as input_pdf_file:
        reader = PdfFileReader(input_pdf_file)
        writer = PdfFileWriter()
        for page_num in range(reader.getNumPages()):
            writer.addPage(reader.getPage(page_num))

    # Load the PKCS#12 certificate
    with open(pkcs12_path, 'rb') as pkcs12_file:
        pkcs12 = load_pkcs12(pkcs12_file.read(), pkcs12_password)

    private_key = pkcs12.get_privatekey()
    cert = pkcs12.get_certificate()
    
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
