package main.figures;

public class Rectangle extends Figure {
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
}
