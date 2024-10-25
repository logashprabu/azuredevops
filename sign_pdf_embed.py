from spire.pdf.common import *
from spire.pdf import *

# Create a PdfDocument object
doc = PdfDocument()

# Load a PDF file
doc.LoadFromFile("input.pdf")

# Specify the path of the pfx certificate
pfxCertificatePath = "certificate.pfx"

# Specify the password of the PDF certificate
pfxPassword = "TerosonIsON0523!"

# Create a signature maker
signatureMaker = PdfOrdinarySignatureMaker(doc, pfxCertificatePath, pfxPassword)

# Show validity symbol in signature
#signatureMaker.SetAcro6Layers(False)

# Get the signature
signature = signatureMaker.Signature

# Configure the signature properties
signature.Name = "Alexander"
signature.ContactInfo = "555666"
signature.Location = "U.S."
signature.Reason = "This is the final version."

# Create a custom signature appearance
appearance = PdfSignatureAppearance(signature)

# Set labels for the signature
appearance.NameLabel = "Signer: "
appearance.ContactInfoLabel = "Phone: "
appearance.LocationLabel = "Location: "
appearance.ReasonLabel = "Reason: "

# Load an image for signature appearance
image = PdfImage.FromFile("sample.jpg")

# Set the image as the signature image
appearance.SignatureImage = image

# Set the graphic mode
appearance.GraphicMode = GraphicMode.SignImageAndSignDetail

# Get the last page
page = doc.Pages[doc.Pages.Count - 1]

# Add the signature to a specified location of the page
signatureMaker.MakeSignature("Signature by Alexander", page, 54.0, page.Size.Height - 100.0, 240.0, 80.0, appearance)

# Save the signed document
doc.SaveToFile("DisplayValiditySymbol.pdf")

# Dispose resources
doc.Dispose()
