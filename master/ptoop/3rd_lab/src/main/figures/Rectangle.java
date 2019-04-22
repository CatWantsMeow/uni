package main.figures;

import main.serialization.Serializer;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Rectangle extends Figure {
    public Rectangle() {
        this.points = new Point[]{new Point(), new Point()};
    }

    public Rectangle(Point ltc, Point rbc) {
        this.points = new Point[]{ltc, rbc};
    }

    @Override
    public String represent() {
        return String.format(
                "Rectangle(left top point: %s, right bottom point: %s)",
                this.points[0].represent(),
                this.points[1].represent()
        );
    }

    @Override
    public void input() {
        System.out.println("Enter a left top point:");
        this.points[0].input();

        System.out.println("Enter a right bottom point:");
        this.points[1].input();
    }

    @Override
    public String serialize() {
        return String.format(
                "<lt-point>%s</lt-point><rb-point>%s</rb-point>",
                this.points[0].serialize(),
                this.points[1].serialize()
        );
    }

    @Override
    public void deserialize(String str) throws Exception {
        String pattern = String.format(
                "\\s*<lt-point>%s</lt-point>\\s*<rb-point>%s</rb-point>\\s*",
                Serializer.STR_PATTERN, Serializer.STR_PATTERN
        );

        Matcher m = Pattern.compile(pattern, Pattern.DOTALL).matcher(str);
        if (!m.matches())throw new Exception();

        this.points[0].deserialize(m.group(1));
        this.points[1].deserialize(m.group(2));
    }
}
