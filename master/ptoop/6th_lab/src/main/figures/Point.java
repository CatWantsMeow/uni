package main.figures;

import main.console.InputHelper;
import main.serialization.Serializer;

import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

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

    @Override
    public String serialize() {
        return String.format(
                "<x>%f</x><y>%f</y>",
                this.x, this.y
        );
    }

    @Override
    public void deserialize(String str) throws Exception {
        String pattern = String.format(
                "\\s*<x>%s</x>\\s*<y>%s</y>\\s*",
                Serializer.DOUBLE_PATTERN, Serializer.DOUBLE_PATTERN
        );

        Matcher m = Pattern.compile(pattern, Pattern.DOTALL).matcher(str);
        if (!m.matches()) throw new Exception();

        this.x = Double.valueOf(m.group(1));
        this.y = Double.valueOf(m.group(2));
    }
}
