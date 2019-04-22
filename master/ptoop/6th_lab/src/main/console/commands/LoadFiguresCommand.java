package main.console.commands;

import main.console.InputHelper;
import main.console.ObjectManager;
import main.serialization.ISerializationProcessor;
import main.serialization.Serializer;

import java.io.BufferedReader;
import java.io.FileReader;
import java.util.Scanner;
import java.util.stream.Collectors;

public class LoadFiguresCommand extends Command {
    public LoadFiguresCommand(ObjectManager manager) {
        super(manager);
    }

    @Override
    public void execute() {
        System.out.println();

        ISerializationProcessor processor = null;
        if (this.manager.processors.size() == 1) {
            processor = this.manager.processors.get(0);
        }
        else if (this.manager.processors.size() > 1) {
            for (int i = 0; i < this.manager.processors.size(); i++) {
                System.out.printf(
                        "#%d - %s\n",
                        i,
                        this.manager.processors.get(i).getClass().getSimpleName()
                );
            }
            int i = InputHelper.enterInt(": ");
            if (i < 0 || i >= this.manager.processors.size()) {
                System.out.println("Invalid :C");
                return;
            }
            processor = this.manager.processors.get(i);
        }

        Scanner scanner = new Scanner(System.in);
        System.out.print("Filename: ");
        String fileName = scanner.nextLine();


        try {
            BufferedReader reader = new BufferedReader(new FileReader(fileName));
            String data = reader.lines().collect(Collectors.joining("\n"));
            reader.close();

            this.manager.objects = Serializer.deserialize(data, processor);
        } catch (Exception e) {
            System.out.printf("Failed to load data from file (%s) :C\n", e.toString());
            return;
        }
        System.out.println("Figures are loaded.");
    }

    @Override
    public String getName() {
        return "Load figures";
    }
}
