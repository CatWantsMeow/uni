package main.figures;

import java.util.Scanner;

public class Circle extends Figure {
    public double radius;

    public Circle() {
        this.points = new Point[]{new Point()};
    }

    public Circle(Point center, double radius) {
        this.points = new Point[]{center};
        this.radius = radius;
    }

    @Override
    public String represent() {
        return String.format(
                "Circle(center: %s, radius: %.2f)",
                this.points[0].represent(),
                this.radius
        );
    }

    @Override
    public void input() {
        System.out.println("Enter a center point:");
        this.points[0].input();

        System.out.println("Enter a radius:");
        Scanner s = new Scanner(System.in);
        this.radius = s.nextDouble();
    }
}
