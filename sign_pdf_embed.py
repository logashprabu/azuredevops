from pyhanko.sign import signers
from pyhanko_certvalidator import ValidationContext
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.backends import default_backend

def load_private_key_from_pkcs12(p12_file_path, password=None):
    with open(p12_file_path, "rb") as p12_file:
        private_key, certificate, additional_certs = pkcs12.load_key_and_certificates(
            p12_file.read(), password.encode() if password else None, backend=default_backend()
        )
        return private_key, certificate, additional_certs

def sign_pdf(input_pdf, output_pdf, private_key_path, password=None):
    # Load the private key and certificate
    private_key, certificate, additional_certs = load_private_key_from_pkcs12(private_key_path, password)

    # Create the signer
    signer = signers.SimpleSigner(
        signing_cert=certificate,
        signing_key=private_key,
        cert_registry=signers.SimpleCertificateStore([certificate] + additional_certs),
        signature_mechanism=signers.PdfSignatureMetadata()
    )

    # Sign the PDF
    with open(input_pdf, 'rb') as pdf_file:
        writer = signers.PdfSigner(signer)
        writer.sign_pdf(pdf_file, output_pdf)

if __name__ == "__main__":
    # Paths to the private key and the PDF files
    input_pdf_path = "input.pdf"
    output_pdf_path = "digitally_signed_document.pdf"
    private_key_path = "private_key.p12"  # Specify your PKCS12 (.p12) private key path

    # Optional password for private key (if encrypted)
    password = "password"  # Use None if there is no password

    # Call the function to sign the PDF
    sign_pdf(input_pdf_path, output_pdf_path, private_key_path, password=password)
