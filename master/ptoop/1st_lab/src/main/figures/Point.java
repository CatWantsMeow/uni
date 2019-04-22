package main.figures;

public class Point extends Figure {
    public double x;
    public double y;

    public Point(double x, double y) {
        this.x = x;
        this.y = y;
    }

    @Override
    public String represent() {
        return String.format("(%.2f, %.2f)", this.x, this.y);
    }
}
