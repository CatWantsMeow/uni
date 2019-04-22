package main.serialization;

import java.lang.reflect.Constructor;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Serializer {
    public static final String DOUBLE_PATTERN = "\\s*([+-]?[0-9]*[.]?[0-9]+)\\s*";
    public static final String STR_PATTERN = "\\s*(.+?)\\s*";

    public static String serialize(List<ISerializable> objects, ISerializationProcessor processor) throws Exception {
        StringBuilder data = new StringBuilder();
        for (ISerializable obj : objects) {
            String xml = obj.serialize();
            data.append(String.format(
                    "<object type=\"%s\">%s</object>",
                    obj.getClass().getName(),
                    xml
            ));
        }

        String res = "<objects>" + data.toString() + "</objects>";
        if (processor != null) {
            res = processor.postSerialize(res);
        }
        return res;
    }

    public static List<ISerializable> deserialize(String str, ISerializationProcessor processor) throws Exception {
        if (processor != null) {
            str = processor.preDeserialize(str);
        }

        String p = "\\s*<objects>" + STR_PATTERN + "</objects>\\s*";
        Matcher m = Pattern.compile(p, Pattern.DOTALL).matcher(str);
        if (!m.matches()) throw new Exception();

        p = "<object type=\"(.+?)\">(.*?)</object>";
        m = Pattern.compile(p, Pattern.DOTALL).matcher(m.group(1));

        List<ISerializable> objects = new ArrayList<>();
        while (m.find()) {
            String type = m.group(1);
            try {
                Class<?> shapeType = Class.forName(type);
                Constructor<?> constructor = shapeType.getConstructor();
                ISerializable obj = (ISerializable) constructor.newInstance();
                obj.deserialize(m.group(2));
                objects.add(obj);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        return objects;
    }
}
