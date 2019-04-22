package main.plugins;

import java.io.File;
import java.io.FileFilter;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLClassLoader;
import java.util.ArrayList;
import java.util.List;

public class PluginLoader {
    private static class ModuleFilter implements FileFilter {
        @Override
        public boolean accept(File file) {
            return (
                    file.isFile() &&
                    file.getName().toLowerCase().endsWith(".class")
            );
        }
    }

    public static List<Class<?>> loadPlugins(String directory) {
        List<Class<?>> classes = new ArrayList<>();
        File[] files = new File(directory).listFiles(new ModuleFilter());
        if (files == null) {
            System.out.printf("Failed to locate '%s' directory :C\n", directory);
            return classes;
        }

        for (File f : files) {
            URL loadPath = null;
            try {
                loadPath = f.toURI().toURL();
            } catch (MalformedURLException e) {
                e.printStackTrace();
            }

            URL[] classUrl = new URL[]{loadPath};
            ClassLoader cl = new URLClassLoader(classUrl);
            try {
                String className = f.getName().split("[.]")[0];
                Class<?> loadedClass = cl.loadClass("plugins." + className);
                classes.add(loadedClass);
            } catch (Exception e) {
                System.out.printf(
                        "Failed to load '%s' plugin (%s) :C\n",
                        f.getName(), e.toString()
                );
            }
        }
        return classes;
    }
}