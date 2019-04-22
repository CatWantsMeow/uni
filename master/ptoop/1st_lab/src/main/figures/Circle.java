package main.figures;

public class Circle extends Figure {
    public double radius;

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
}
