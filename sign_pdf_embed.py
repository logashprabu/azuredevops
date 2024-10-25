import pikepdf
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.asymmetric.utils import Prehashed

def load_private_key(private_key_path, password=None):
    with open(private_key_path, "rb") as key_file:
        return load_pem_private_key(key_file.read(), password=password)

def sign_pdf(input_pdf, output_pdf, private_key_path, password=None):
    # Load the private key
    private_key = load_private_key(private_key_path, password)

    # Open the PDF
    with pikepdf.open(input_pdf) as pdf:
        # Create a new signature dictionary in the PDF
        pdf.signatures.append()
        
        # Extract some content for demonstration purposes (actual content selection may vary)
        page = pdf.pages[0]
        content_to_sign = page.extract_text().encode('utf-8')

        # Create the digital signature
        signature = private_key.sign(
            content_to_sign,
            padding.PKCS1v15(),
            Prehashed(hashes.SHA256())
        )

        # Save the signed PDF
        pdf.save(output_pdf)
    
    print(f"PDF successfully signed and saved as: {output_pdf}")

if __name__ == "__main__":
    # Paths to the private key and the PDF files
    input_pdf_path = "document_to_sign.pdf"
    output_pdf_path = "digitally_signed_document.pdf"
    private_key_path = "private_key.pem"  # Specify your private key path

    # Optional password for private key (if encrypted)
    password = None  # Or, use "your-password".encode() if using an encrypted key

    # Call the function to sign the PDF
    sign_pdf(input_pdf_path, output_pdf_path, private_key_path, password=password)
