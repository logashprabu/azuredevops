# sign_pdf_embed.py

import PyPDF2
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.exceptions import InvalidKey
import os

def sign_pdf(input_pdf, output_pdf, cert_file, key_file, key_password):
    # Read the PDF
    with open(input_pdf, "rb") as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        writer = PyPDF2.PdfWriter()
        writer.append_pages_from_reader(reader)

        # Create a placeholder for the signature (in a real implementation, you'd adjust this section)
        writer.add_metadata({
            "/Title": "Signed PDF",
            "/Subject": "This PDF has been digitally signed"
        })

        # Read the private key
        with open(key_file, "rb") as key:
        try:
            # Try loading the key with the password (if encrypted)
            private_key = load_pem_private_key(key.read(), password=key_password.encode())
        except InvalidKey:
            # If it fails, assume the key is not encrypted (common case)
            key.seek(0)  # Reset the file pointer
            private_key = load_pem_private_key(key.read(), password=None)


        # Generate a signature (simplified version for demonstration)
        data_to_sign = b"Sample data to sign"  # Replace with actual data to be signed
        signature = private_key.sign(
            data_to_sign,
            padding.PKCS1v15(),
            hashes.SHA256()
        )

        # Embed the signature as metadata (for demonstration only)
        writer.add_metadata({
            "/Signature": signature.hex()  # Convert signature to hexadecimal string
        })

        # Write the signed PDF
        with open(output_pdf, "wb") as signed_pdf:
            writer.write(signed_pdf)

    print(f"Signed PDF created at: {output_pdf}")

# Example usage
if __name__ == "__main__":
    sign_pdf("input.pdf", "signed_output.pdf", "certificate.crt", "private.key", "TerosonIsON0523!")
