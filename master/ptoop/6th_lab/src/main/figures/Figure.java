package main.figures;

import main.serialization.ISerializable;

public abstract class Figure implements ISerializable {
    public Point[] points;

    public abstract String represent();

    public abstract void input();
}
