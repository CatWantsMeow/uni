package main.console.commands;

import main.console.InputHelper;
import main.console.ObjectManager;
import main.figures.Figure;

import java.lang.reflect.Constructor;

public class CreateFigureCommand extends Command {
    public CreateFigureCommand(ObjectManager manager) {
        super(manager);
    }

    @Override
    public void execute() {
        System.out.println();
        for (int i = 0; i < this.manager.types.size(); i++) {
            System.out.printf(
                    "#%d - %s\n",
                    i,
                    this.manager.types.get(i).getSimpleName()
            );
        }

        int i = InputHelper.enterInt(": ");
        if (i < 0 || i >= this.manager.types.size()) {
            System.out.println("Invalid :C");
        } else {
            System.out.println();
            try {
                Constructor<?> constructor = this.manager.types.get(i).getConstructor();
                Figure shape = (Figure) constructor.newInstance();
                shape.input();

                this.manager.objects.add(shape);
                System.out.printf("%s created.\n", shape.represent());
            } catch (Exception e) {
                System.out.printf("Failed to create a figure (%s) :C\n", e.toString());
            }
        }

    }

    @Override
    public String getName() {
        return "Create a figure";
    }
}
