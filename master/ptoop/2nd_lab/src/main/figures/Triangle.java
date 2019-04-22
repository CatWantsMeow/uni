package main.figures;

public class Triangle extends Figure {
    public Triangle() {
        this.points = new Point[]{new Point(), new Point(), new Point()};
    }

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

    @Override
    public void input() {
        System.out.println("Enter the first point:");
        this.points[0].input();

        System.out.println("Enter the second point:");
        this.points[1].input();

        System.out.println("Enter the third point:");
        this.points[2].input();
    }
}
