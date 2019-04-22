package main;

import main.figures.*;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Main {
    private static List<Figure> init() {
        return new ArrayList<>(Arrays.asList(
            new Line(new Point(3.2, -1.2), new Point(1, 3)),
            new Line(new Point(0, -2), new Point(3, -2.33)),
            new Line(new Point(-2.3, -1.2), new Point(1.23, 2.23)),

            new Triangle(new Point(0, 0), new Point(-1, 0), new Point(0, -1)),
            new Triangle(new Point(2, -3.2), new Point(-1.2, -2), new Point(3, 2)),

            new Polygon(new Point[]{}),
            new Polygon(new Point[]{ new Point(0, 0), new Point(1, 0), new Point(2, 3.1) }),

            new Rectangle(new Point(-1, -2), new Point(2, 1)),
            new Rectangle(new Point(-2.3, -3.1), new Point(1, 3.2)),

            new Circle(new Point(0, 0), 1),
            new Circle(new Point(-1.2, -1), 23.3)
        ));
    }

    public static void main(String[] args) {
        List<Figure> figures = Main.init();

        for (int i = 0; i < figures.size(); i++) {
            System.out.printf("%d. %s\n", i, figures.get(i).represent());
            System.out.println();
        }
    }
}
