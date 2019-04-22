package main.console.commands;

import main.console.InputHelper;
import main.console.ObjectManager;
import main.figures.Figure;

public class UpdateFigureCommand extends Command {
    public UpdateFigureCommand(ObjectManager manager) {
        super(manager);
    }

    @Override
    public void execute() {
        new ListFiguresCommand(this.manager).execute();
        if (this.manager.objects.size() == 0) return;

        int i = InputHelper.enterInt(": ");
        if (i < 0 || i >= this.manager.objects.size()) {
            System.out.println("Invalid :C");
        } else {
            try {
                Figure shape = (Figure) this.manager.objects.get(i);
                shape.input();

                System.out.printf("%s updated.\n", shape.represent());
            } catch (Exception e) {
                System.out.printf("Failed to update the figure (%s) :C\n", e.toString());
            }
        }
    }

    @Override
    public String getName() {
        return "Update a figure";
    }
}
