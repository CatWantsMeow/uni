package main.figures;

public class Triangle extends Figure {
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
}
