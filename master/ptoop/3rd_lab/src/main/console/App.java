package main.console;

import main.console.commands.*;
import main.figures.*;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class App {
    private ObjectManager manager;
    private List<Command> commands;

    public App() {
        this.manager = new ObjectManager(Arrays.asList(
                Rectangle.class,
                Line.class,
                Triangle.class,
                Circle.class,
                Polygon.class
        ));

        this.commands = new ArrayList<>(Arrays.asList(
                new ListFiguresCommand(this.manager),
                new CreateFigureCommand(this.manager),
                new UpdateFigureCommand(this.manager),
                new DeleteFigureCommand(this.manager),
                new LoadFiguresCommand(this.manager),
                new DumpFiguresCommand(this.manager)
        ));

        this.init();
    }

    private void init() {
        this.manager.objects = new ArrayList<>(Arrays.asList(
                new Line(new Point(3.2, -1.2), new Point(1, 3)),
                new Line(new Point(0, -2), new Point(3, -2.33)),
                new Line(new Point(-2.3, -1.2), new Point(1.23, 2.23)),

                new Triangle(new Point(0, 0), new Point(-1, 0), new Point(0, -1)),
                new Triangle(new Point(2, -3.2), new Point(-1.2, -2), new Point(3, 2)),

                new Polygon(new Point[]{}),
                new Polygon(new Point[]{new Point(0, 0), new Point(1, 0), new Point(2, 3.1)}),

                new Rectangle(new Point(-1, -2), new Point(2, 1)),
                new Rectangle(new Point(-2.3, -3.1), new Point(1, 3.2)),

                new Circle(new Point(0, 0), 1),
                new Circle(new Point(-1.2, -1), 23.3)
        ));
    }

    public void start() {
        while (true) {
            for (int i = 0; i < this.commands.size(); i++) {
                System.out.printf("#%d - %s.\n", i, this.commands.get(i).getName());
            }

            int i = InputHelper.enterInt(": ");
            if (i == -1) {
                break;
            } else if (i < 0 || i >= this.commands.size()) {
                System.out.println("Invalid :C");
            } else {
                this.commands.get(i).execute();
                System.out.println();
            }
        }
    }
}
