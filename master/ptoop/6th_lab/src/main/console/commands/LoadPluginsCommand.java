package main.console.commands;

import main.console.ObjectManager;
import main.figures.Figure;
import main.plugins.PluginLoader;
import main.serialization.ISerializationProcessor;

import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.util.List;

public class LoadPluginsCommand extends Command {
    public LoadPluginsCommand(ObjectManager manager) {
        super(manager);
    }

    @Override
    public void execute() {
        List<Class<?>> classes = PluginLoader.loadPlugins("out/plugins");
        for (Class<?> c: classes) {
            if (Figure.class.isAssignableFrom(c)) {
                if (!this.manager.types.contains(c)) {
                    this.manager.types.add(c);
                }
            }

            if (ISerializationProcessor.class.isAssignableFrom(c)) {
                if (!this.manager.processors.contains(c)) {
                    try {
                        Constructor con = c.getConstructors()[0];
                        this.manager.processors.add((ISerializationProcessor) con.newInstance());
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }

            System.out.printf("Class '%s' loaded.\n", c.getName());
        }
    }

    @Override
    public String getName() {
        return "Load plugins";
    }
}
