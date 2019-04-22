package main.figures;

import main.console.InputHelper;

import java.util.Scanner;

public class Point extends Figure {
    public double x;
    public double y;

    public Point() {
    }

    public Point(double x, double y) {
        this.x = x;
        this.y = y;
    }

    @Override
    public String represent() {
        return String.format("(%.2f, %.2f)", this.x, this.y);
    }

    @Override
    public void input() {
        String in = InputHelper.enterString("Enter point ({x} {y}): ");
        Scanner s = new Scanner(in);
        this.x = s.nextDouble();
        this.y = s.nextDouble();
    }
}
