package main.figures;

import main.serialization.Serializer;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Line extends Figure {
    public Line() {
        this.points = new Point[]{new Point(), new Point()};
    }

    public Line(Point start, Point end) {
        this.points = new Point[]{start, end};
    }

    @Override
    public String represent() {
        return String.format(
                "Line(start: %s, end: %s)",
                this.points[0].represent(),
                this.points[1].represent()
        );
    }

    @Override
    public void input() {
        System.out.println("Enter a start point");
        this.points[0].input();

        System.out.println("Enter an end point:");
        this.points[1].input();
    }

    @Override
    public String serialize() {
        return String.format(
                "<start>%s</start><end>%s</end>",
                this.points[0].serialize(),
                this.points[1].serialize()
        );
    }

    @Override
    public void deserialize(String str) throws Exception {
        String pattern = String.format(
                "\\s*<start>%s</start>\\s*<end>%s</end>\\s*",
                Serializer.STR_PATTERN, Serializer.STR_PATTERN
        );

        Matcher m = Pattern.compile(pattern, Pattern.DOTALL).matcher(str);
        if (!m.matches()) throw new Exception();

        this.points[0].deserialize(m.group(1));
        this.points[1].deserialize(m.group(2));
    }
}
