import aspose.pdf as pdf
import aspose.pydrawing as drawing

def sign_pdf(input_pdf_path, output_pdf_path, cert_path, cert_password):
    # Load the PDF file to crop
    pdfDoc = pdf.Document(input_pdf_path)

    # Instantiate the PdfFileSignature for the loaded PDF document
    signature = pdf.facades.PdfFileSignature(pdfDoc)

    # Load the certificate file along with the password
    pkcs = pdf.forms.PKCS7(cert_path, cert_password)

    # Assign the access permissions
    docMdpSignature = pdf.forms.DocMDPSignature(pkcs, pdf.forms.DocMDPAccessPermissions.FILLING_IN_FORMS)

    # Set the rectangle for the signature placement
    rect = drawing.Rectangle(150, 650, 450, 150)

    # Set signature appearance
    signature.signature_appearance = "sample.jpg"  # Update with your signature image path

    # Sign the PDF file with the certify method
    signature.certify(1, "Signature Insert Reason", "Contact", "Location", True, rect, docMdpSignature)

    # Save digitally signed PDF file 
    signature.save(output_pdf_path)

    print("PDF successfully signed and saved as:", output_pdf_path)

if __name__ == "__main__":
    # Paths to the PDF file, certificate, and output file
    input_pdf_path = "input.pdf"  # Specify your input PDF path
    output_pdf_path = "Signed_PDF.pdf"  # Specify your output PDF path
    cert_path = "certificate.p12"  # Specify your certificate path
    cert_password = "password"  # Specify your certificate password

    # Call the function to sign the PDF
    sign_pdf(input_pdf_path, output_pdf_path, cert_path, cert_password)
