package main.figures;

public class Line extends Figure {
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
}
