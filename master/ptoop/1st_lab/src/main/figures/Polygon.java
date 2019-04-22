package main.figures;

import java.util.List;
import java.util.ArrayList;

public class Polygon extends Figure {
    public Polygon(Point[] points) {
        this.points = points;
    }

    @Override
    public String represent() {
        if (this.points.length == 0) {
            return "Polygon(points: empty)";
        }

        List<String> out = new ArrayList<>();
        for (Point point: this.points) {
            out.add(point.represent());
        }
        return "Polygon(points: " + String.join(", ", out) + ")";
    }
}
