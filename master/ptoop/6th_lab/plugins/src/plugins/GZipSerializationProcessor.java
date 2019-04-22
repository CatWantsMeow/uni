package plugins;

import main.serialization.ISerializationProcessor;

import java.io.ByteArrayOutputStream;
import java.io.ByteArrayInputStream;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.zip.GZIPOutputStream;
import java.util.zip.GZIPInputStream;

public class GZipSerializationProcessor implements ISerializationProcessor {
    public GZipSerializationProcessor() { }

    @Override
    public String postSerialize(String str) throws Exception {
        try (ByteArrayOutputStream out = new ByteArrayOutputStream())
        {
           try (GZIPOutputStream gzip = new GZIPOutputStream(out))
           {
               gzip.write(str.getBytes());
           }

           Hash hash = new Hash();
           return hash.appendHash(out.toString("ISO-8859-1"));
        }
    }

    @Override
    public String preDeserialize(String str) throws Exception {
        Hash hash = new Hash();
        if (!hash.checksum(str)) {
            throw new Exception("Arhive was modified");
        }
        str = hash.removeHash(str);

        ByteArrayOutputStream out = new ByteArrayOutputStream();
        ByteArrayInputStream in = new ByteArrayInputStream(str.getBytes("ISO-8859-1"));
        try (GZIPInputStream gzip = new GZIPInputStream(in)) {
            int b;
            while ((b = gzip.read()) != -1) {
                out.write((byte) b);
            }
            return new String(out.toByteArray());
        }
    }


}
