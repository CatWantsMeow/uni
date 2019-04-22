package main.figures;

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
}
