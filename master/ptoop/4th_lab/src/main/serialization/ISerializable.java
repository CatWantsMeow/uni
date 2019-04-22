package main.serialization;

public interface ISerializable {
    String serialize();
    void deserialize(String str) throws Exception;
}
