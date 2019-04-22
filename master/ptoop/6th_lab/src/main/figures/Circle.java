package main.figures;

import main.serialization.Serializer;

import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

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

    @Override
    public String serialize() {
        return String.format(
                "<center>%s</center><radius>%f</radius>",
                this.points[0].serialize(),
                this.radius
        );
    }

    @Override
    public void deserialize(String str) throws Exception {
        String pattern = String.format(
                "\\s*<center>%s</center>\\s*<radius>%s</radius>\\s*",
                Serializer.STR_PATTERN, Serializer.DOUBLE_PATTERN
        );

        Matcher m = Pattern.compile(pattern, Pattern.DOTALL).matcher(str);
        if (!m.matches()) throw new Exception();

        this.points[0].deserialize(m.group(1));
        this.radius = Double.valueOf(m.group(2));
    }
}
