package plugins;

import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.security.Key;
import java.util.Base64;

class AES {
    private final String KEY = "secret-key-12345";
    private final String ALGO = "AES";

    public String processOnDump(String data) throws Exception {
        Key key = new SecretKeySpec(this.KEY.getBytes(), this.ALGO);

        Cipher cipher = Cipher.getInstance(this.ALGO);
        cipher.init(Cipher.ENCRYPT_MODE, key);
        byte[] processed = cipher.doFinal(data.getBytes());

        byte[] encoded = Base64.getEncoder().encode(processed);
        return new String(encoded);
    }

    public String processOnLoad(String data) throws Exception {
        byte[] decoded = Base64.getDecoder().decode(data);

        Key key = new SecretKeySpec(this.KEY.getBytes(), this.ALGO);
        Cipher c = Cipher.getInstance(ALGO);
        c.init(Cipher.DECRYPT_MODE, key);
        byte[] processed = c.doFinal(decoded);

        return new String(processed);
    }
}
