package main.figures;

import main.serialization.Serializer;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Triangle extends Figure {
    public Triangle() {
        this.points = new Point[]{new Point(), new Point(), new Point()};
    }

    public Triangle(Point p1, Point p2, Point p3) {
        this.points = new Point[]{p1, p2, p3};
    }

    @Override
    public String represent() {
        return String.format(
                "Triangle(point1: %s, point2: %s, point3: %s)",
                this.points[0].represent(),
                this.points[1].represent(),
                this.points[2].represent()
        );
    }

    @Override
    public void input() {
        System.out.println("Enter the first point:");
        this.points[0].input();

        System.out.println("Enter the second point:");
        this.points[1].input();

        System.out.println("Enter the third point:");
        this.points[2].input();
    }

    @Override
    public String serialize() {
        return String.format(
                "<point1>%s</point1><point2>%s</point2><point3>%s</point3>",
                this.points[0].serialize(),
                this.points[1].serialize(),
                this.points[2].serialize()
        );
    }

    @Override
    public void deserialize(String str) throws Exception {
        String pattern = String.format(
                "\\s*<point1>%s</point1>" +
                        "\\s*<point2>%s</point2>" +
                        "\\s*<point3>%s</point3>\\s*",
                Serializer.STR_PATTERN,
                Serializer.STR_PATTERN,
                Serializer.STR_PATTERN
        );

        Matcher m = Pattern.compile(pattern, Pattern.DOTALL).matcher(str);
        if (!m.matches()) throw new Exception();

        this.points[0].deserialize(m.group(1));
        this.points[1].deserialize(m.group(2));
        this.points[2].deserialize(m.group(3));
    }
}
