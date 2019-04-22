package main.console.commands;

import main.console.ObjectManager;
import main.serialization.Serializer;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.util.Scanner;

public class DumpFiguresCommand extends Command {
    public DumpFiguresCommand(ObjectManager manager) {
        super(manager);
    }

    @Override
    public void execute() {
        System.out.println();

        Scanner scanner = new Scanner(System.in);
        System.out.print("Filename: ");
        String fileName = scanner.nextLine();

        try {
            BufferedWriter writer = new BufferedWriter(new FileWriter(fileName));
            writer.write(Serializer.serialize(this.manager.objects));
            writer.close();
        } catch (Exception e) {
            System.out.printf("Failed to dump data to file (%s) :C\n", e.toString());
            return;
        }
        System.out.println("Figures is saved.");
    }

    @Override
    public String getName() {
        return "Dump figures";
    }
}
