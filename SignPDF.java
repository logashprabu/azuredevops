// Save this as SignPDF.java
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.pdmodel.interactive.digitalsignature.PDSignature;
import org.apache.pdfbox.pdmodel.interactive.digitalsignature.SignatureOptions;
import org.bouncycastle.cert.jcajce.JcaCertStore;
import org.bouncycastle.cms.CMSSignedDataGenerator;
import org.bouncycastle.cms.jcajce.JcaSignerInfoGeneratorBuilder;
import org.bouncycastle.operator.jcajce.JcaContentSignerBuilder;
import org.bouncycastle.operator.jcajce.JcaDigestCalculatorProviderBuilder;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.security.KeyStore;
import java.security.PrivateKey;
import java.security.cert.Certificate;
import java.util.Arrays;
import java.util.Calendar;

public class SignPDF {
    public static void main(String[] args) throws Exception {
        PDDocument document = PDDocument.load(new FileInputStream("input.pdf"));
        PDSignature signature = new PDSignature();
        signature.setFilter(PDSignature.FILTER_ADOBE_PPKLITE);
        signature.setSubFilter(PDSignature.SUBFILTER_ADBE_PKCS7_DETACHED);
        signature.setName("User Name");
        signature.setLocation("Location");
        signature.setReason("Reason for signing");
        signature.setSignDate(Calendar.getInstance());

        KeyStore keystore = KeyStore.getInstance("PKCS12");
        keystore.load(new FileInputStream("certificate.pfx"), "password".toCharArray());
        PrivateKey privateKey = (PrivateKey) keystore.getKey("alias", "password".toCharArray());
        Certificate[] certificateChain = keystore.getCertificateChain("alias");

        SignatureOptions signatureOptions = new SignatureOptions();
        document.addSignature(signature, new SignatureInterface() {
            public byte[] sign(InputStream content) throws SignatureException {
                try {
                    JcaContentSignerBuilder builder = new JcaContentSignerBuilder("SHA256WithRSA");
                    builder.setProvider("BC");
                    CMSSignedDataGenerator gen = new CMSSignedDataGenerator();
                    gen.addSignerInfoGenerator(new JcaSignerInfoGeneratorBuilder(
                            new JcaDigestCalculatorProviderBuilder().setProvider("BC").build())
                            .build(builder.build(privateKey), (X509Certificate) certificateChain[0]));
                    gen.addCertificates(new JcaCertStore(Arrays.asList(certificateChain)));
                    return gen.generate(content, false).getEncoded();
                } catch (Exception e) {
                    throw new SignatureException("Error while creating PKCS7 signature", e);
                }
            }
        }, signatureOptions);
        document.save("signed_output.pdf");
        document.close();
    }
}
