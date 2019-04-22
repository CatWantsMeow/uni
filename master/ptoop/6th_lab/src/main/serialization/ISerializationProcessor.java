package main.serialization;

public interface ISerializationProcessor {
    String postSerialize(String str) throws Exception;
    String preDeserialize(String str) throws Exception;
}
