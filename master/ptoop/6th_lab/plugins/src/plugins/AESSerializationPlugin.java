package plugins;

import main.serialization.ISerializationProcessor;

import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.security.Key;
import java.util.Base64;

public class AESSerializationPlugin implements ISerializationProcessor {
    public AESSerializationPlugin() {}

    @Override
    public String postSerialize(String str) throws Exception {
        AES processor = new AES();
        return processor.processOnDump(str);
    }

    @Override
    public String preDeserialize(String str) throws Exception {
        AES processor = new AES();
        return processor.processOnLoad(str);
    }
}
