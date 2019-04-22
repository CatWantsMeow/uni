package main.console.commands;

import main.console.ObjectManager;
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

        Scanner scanner = new Scanner(System.in);
        System.out.print("Filename: ");
        String fileName = scanner.nextLine();

        try {
            BufferedReader reader = new BufferedReader(new FileReader(fileName));
            String data = reader.lines().collect(Collectors.joining());
            reader.close();

            this.manager.objects = Serializer.deserialize(data);
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
