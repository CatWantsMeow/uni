package main.figures;

import main.console.InputHelper;

import java.util.ArrayList;
import java.util.List;

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
}
