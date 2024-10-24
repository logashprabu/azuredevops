#!/bin/bash

# Exit on any error
set -e

# Arguments passed to the script
INPUT_PDF=$1
CERT_PATH=$2
KEY_PATH=$3
PASSPHRASE=$4
OUTPUT_PDF="signed_output.pdf"
SIGNATURE_FILE="signature.sha256"
SIGNED_PDF="signed_output.pdf"

# Ensure all arguments are provided
if [ -z "$INPUT_PDF" ] || [ -z "$CERT_PATH" ] || [ -z "$KEY_PATH" ] || [ -z "$PASSPHRASE" ]; then
  echo "Usage: $0 <input_pdf> <cert_path> <key_path> <passphrase>"
  exit 1
fi

# Check if OpenSSL is installed
if ! command -v openssl &> /dev/null; then
  echo "OpenSSL could not be found. Please install OpenSSL to proceed."
  exit 1
fi

# Generate a SHA256 signature of the PDF using the private key
openssl dgst -sha256 -sign "$KEY_PATH" -passin pass:"$PASSPHRASE" -out "$SIGNATURE_FILE" "$INPUT_PDF"
echo "Generated SHA256 signature: $SIGNATURE_FILE"

# Create a PKCS#7 signature file (this is a detached signature for demo purposes)
openssl smime -sign -in "$SIGNATURE_FILE" -signer "$CERT_PATH" -inkey "$KEY_PATH" -outform DER -out "$SIGNATURE_FILE.p7s" -passin pass:"$PASSPHRASE"
echo "Created PKCS#7 signature: $SIGNATURE_FILE.p7s"

# For simplicity, copy the original PDF to a new file as a placeholder for signing
# In reality, you'd use a dedicated PDF library to properly attach the signature
cp "$INPUT_PDF" "$SIGNED_PDF"
echo "Created signed PDF (placeholder): $SIGNED_PDF"

# Clean up temporary signature file
rm -f "$SIGNATURE_FILE"

echo "PDF signing process completed successfully."
