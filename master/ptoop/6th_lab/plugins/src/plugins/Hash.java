package plugins;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

class Hash {
        public static final int SUM_LENGTH = 64;

        public String toHex(byte[] bytes) {
            StringBuffer result = new StringBuffer();
            for (byte byt : bytes) {
                result.append(Integer.toString((byt & 0xff) + 0x100, 16).substring(1));
            }
            return result.toString();
        }

        public String appendHash(String data) {
            try {
                MessageDigest digest = MessageDigest.getInstance("SHA-256");
                byte[] hash = digest.digest(data.getBytes(StandardCharsets.UTF_8));
                return this.toHex(hash) + data;
            } catch (NoSuchAlgorithmException e) {
                return data;
            }
        }

        public String removeHash(String data) {
            return data.substring(this.SUM_LENGTH);
        }

        public boolean checksum(String data) {
            String oldHash = data.substring(0, SUM_LENGTH);
            data = data.substring(SUM_LENGTH);

            try {
                MessageDigest digest = MessageDigest.getInstance("SHA-256");
                byte[] hash = digest.digest(data.getBytes());
                return this.toHex(hash).equals(oldHash);
            } catch (NoSuchAlgorithmException e) {
                return false;
            }
        }
    }