package main.console;

import java.util.ArrayList;
import java.util.List;

public class ObjectManager {
    public List<Class<?>> types;
    public List<Object> objects;

    public ObjectManager(List<Class<?>> types) {
        this(types, new ArrayList<>());
    }

    public ObjectManager(List<Class<?>> types, List<Object> objects) {
        this.types = types;
        this.objects = objects;
    }
}
