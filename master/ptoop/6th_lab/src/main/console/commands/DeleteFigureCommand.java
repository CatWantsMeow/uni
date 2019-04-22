package main.console.commands;

import main.console.InputHelper;
import main.console.ObjectManager;
import main.figures.Figure;

public class DeleteFigureCommand extends Command {
    public DeleteFigureCommand(ObjectManager manager) {
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
            Figure shape = (Figure) this.manager.objects.get(i);
            this.manager.objects.remove(i);
            System.out.printf("%s deleted.\n", shape.represent());
        }
    }

    @Override
    public String getName() {
        return "Delete a figure";
    }
}
