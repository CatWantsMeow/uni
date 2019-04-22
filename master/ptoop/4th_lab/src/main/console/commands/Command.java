package main.console.commands;


import main.console.ObjectManager;

public abstract class Command {
    public ObjectManager manager;

    Command(ObjectManager manager) {
        this.manager = manager;
    }

    public abstract void execute();

    public abstract String getName();
}
