package main.console.commands;

import main.console.ObjectManager;
import main.figures.Figure;

public class ListFiguresCommand extends Command {
    public ListFiguresCommand(ObjectManager manager) {
        super(manager);
    }

    @Override
    public void execute() {
        System.out.println();
        if (this.manager.objects.size() == 0) {
            System.out.println("Empty :C");
            return;
        }

        for (int i = 0; i < this.manager.objects.size(); i++) {
            System.out.printf(
                    "#%d - %s\n",
                    i,
                    ((Figure) this.manager.objects.get(i)).represent()
            );
        }
    }

    @Override
    public String getName() {
        return "List figures";
    }
}
