package main.console.commands;

import main.console.ObjectManager;
import main.plugins.PluginLoader;
import main.figures.Figure;

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

            System.out.printf("Classs '%s' loaded.\n", c.getName());
        }
    }

    @Override
    public String getName() {
        return "Load plugins";
    }
}
