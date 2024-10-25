from pyhanko.sign import signers, fields
from pyhanko_certvalidator import ValidationContext
from cryptography.hazmat.primitives.serialization import load_pem_private_key, pkcs12
from cryptography.hazmat.backends import default_backend

def load_private_key_from_pemder(key_data, password=None):
    """Load a PEM or DER formatted private key with an optional password."""
    return load_pem_private_key(key_data, password=password, backend=default_backend())

def load_private_key_from_pkcs12(p12_file_path, password=None):
    """Load a private key and certificate from a PKCS12 (.p12) file."""
    with open(p12_file_path, "rb") as p12_file:
        private_key, certificate, additional_certs = pkcs12.load_key_and_certificates(
            p12_file.read(), password.encode() if password else None, backend=default_backend()
        )
        return private_key, certificate

def sign_pdf(input_pdf, output_pdf, private_key_path, cert_path, password=None):
    """Sign the PDF with a private key and certificate."""
    # Load the private key and certificate
    private_key, certificate = load_private_key_from_pkcs12(private_key_path, password)
    
    # Create the signer
    signer = signers.SimpleSigner(
        signing_cert=certificate,
        signing_key=private_key,
        cert_registry=signers.SimpleCertificateStore([certificate]),
    )
    
    # Sign the PDF
    with open(input_pdf, 'rb') as pdf_file:
        writer = signers.PdfSigner(
            signer,
            signature_meta=signers.PdfSignatureMetadata(field_name="Signature1"),
            new_field_spec=fields.SigFieldSpec(sig_field_name="Signature1")
        )
        with open(output_pdf, 'wb') as signed_pdf:
            writer.sign_pdf(pdf_file, signed_pdf)

if __name__ == "__main__":
    # Paths to the private key, certificate, and the PDF files
    input_pdf_path = "input.pdf"
    output_pdf_path = "digitally_signed_document.pdf"
    private_key_path = "private_key.p12"  # Specify your PKCS12 (.p12) private key path
    cert_path = "certificate.pem"  # Not required if the private key includes the certificate

    # Optional password for private key (if encrypted)
    password = "password"  # Use None if there is no password

    # Call the function to sign the PDF
    sign_pdf(input_pdf_path, output_pdf_path, private_key_path, cert_path, password=password)
