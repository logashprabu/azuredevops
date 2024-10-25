from pyhanko.sign import signers
from pyhanko.sign.fields import SigFieldSpec
from pyhanko_certvalidator import CertificateValidator
from pyhanko.sign.general import load_private_key_from_pemder

def sign_pdf(input_pdf, output_pdf, private_key_path, cert_path, password=None):
    # Load private key and certificate
    with open(private_key_path, 'rb') as pk_file, open(cert_path, 'rb') as cert_file:
        private_key = load_private_key_from_pemder(pk_file.read(), password=password)
        cert = cert_file.read()

    # Define a signer object using the key and certificate
    signer = signers.SimpleSigner(
        signing_cert=cert,
        signing_key=private_key,
        cert_chain=[cert],  # Provide additional certificates if needed
        prefer_pss=True
    )

    # Sign the PDF
    with open(input_pdf, 'rb') as in_file:
        with open(output_pdf, 'wb') as out_file:
            signers.sign_pdf(
                in_file,
                signature_meta=signers.SignatureMetadata(field_name='Sig1'),
                signer=signer,
                output=out_file
            )

    print(f"PDF successfully signed and saved as: {output_pdf}")

if __name__ == "__main__":
    input_pdf_path = "input.pdf"
    output_pdf_path = "digitally_signed_document.pdf"
    private_key_path = "private_key.pem"  # Replace with your key path
    cert_path = "certificate.pem"  # Replace with your certificate path
    password = None  # Use your private key password if encrypted

    sign_pdf(input_pdf_path, output_pdf_path, private_key_path, cert_path, password=password)
