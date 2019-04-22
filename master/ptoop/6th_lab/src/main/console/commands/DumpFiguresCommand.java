package main.console.commands;

import main.console.InputHelper;
import main.console.ObjectManager;
import main.serialization.ISerializationProcessor;
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

        ISerializationProcessor processor = null;
        if (this.manager.processors.size() == 1) {
            processor = this.manager.processors.get(0);
        }
        else if (this.manager.processors.size() > 0) {
            for (int i = 0; i < this.manager.processors.size(); i++) {
                System.out.printf(
                        "#%d - %s\n",
                        i,
                        this.manager.processors.get(i).getClass().getSimpleName()
                );
            }
            int i = InputHelper.enterInt(": ");
            if (i < 0 || i >= this.manager.types.size()) {
                System.out.println("Invalid :C");
                return;
            }
            processor = this.manager.processors.get(i);
        }

        Scanner scanner = new Scanner(System.in);
        System.out.print("Filename: ");
        String fileName = scanner.nextLine();

        try {
            BufferedWriter writer = new BufferedWriter(new FileWriter(fileName));
            writer.write(Serializer.serialize(this.manager.objects, processor));
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
