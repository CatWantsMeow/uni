package main.figures;

import main.console.InputHelper;
import main.serialization.Serializer;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Polygon extends Figure {
    public Polygon() {
        this.points = new Point[]{};
    }

    public Polygon(Point[] points) {
        this.points = points;
    }

    @Override
    public String represent() {
        if (this.points.length == 0) {
            return "Polygon(points: empty)";
        }

        List<String> out = new ArrayList<>();
        for (Point point : this.points) {
            out.add(point.represent());
        }
        return "Polygon(points: " + String.join(", ", out) + ")";
    }

    @Override
    public void input() {
        int count = InputHelper.enterInt("Enter points count: ");
        this.points = new Point[count];
        for (int i = 0; i < count; i++) {
            this.points[i] = new Point();
            this.points[i].input();
        }
    }

    @Override
    public String serialize() {
        StringBuilder xml = new StringBuilder();
        for (Point point : this.points) {
            xml.append("<point>").append(point.serialize()).append("</point>");
        }
        return xml.toString();
    }

    @Override
    public void deserialize(String str) throws Exception {
        String pattern = "\\s*<point>" + Serializer.STR_PATTERN + "</point>\\s*";
        Matcher m = Pattern.compile(pattern, Pattern.DOTALL).matcher(str);

        List<Point> points = new ArrayList<>();
        while (m.find()) {
            Point point = new Point();
            point.deserialize(m.group(1));
            points.add(point);
        }
        this.points = points.toArray(new Point[]{});
    }
}
