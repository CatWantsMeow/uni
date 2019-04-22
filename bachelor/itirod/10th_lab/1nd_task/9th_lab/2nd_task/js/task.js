class Task {

    constructor(name, description, start_date, end_date, subTasks) {
        this.name = name;
        this.description = description;
        this.start_date = start_date;
        this.end_date = end_date;
        this.subTasks = subTasks;
    }

    addSubTask(task) {
        this.subTasks.push(task);
    }

    toString() {
        return this.name + "(" + this.description + "): " + this.start_date + " - " + this.end_date;
    }
}


class RunningTask extends Task {
    constructor(...args) {
        super(...args);
        this.completed = false;
        this.state = 0;
    }

    compelete() {
        this.completed = true;
        this.state = 100;
    }
}


task = new RunningTask("Work", "Some work", Date(), Date(), [])
alert(task);
