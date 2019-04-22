package main.figures;

public class Rectangle extends Figure {
    public Rectangle() {
        this.points = new Point[]{new Point(), new Point()};
    }

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

    @Override
    public void input() {
        System.out.println("Enter a left top point:");
        this.points[0].input();

        System.out.println("Enter a right bottom point:");
        this.points[1].input();
    }
}
