function Task(name, description, start_date, end_date, subTasks) {
    this.name = name;
    this.description = description;
    this.start_date = start_date;
    this.end_date = end_date;
    this.subTasks = subTasks;
}

Task.prototype.addSubTask = function (task) {
    this.subTasks.push(task);
};

Task.prototype.toString = function () {
    return this.name + "(" + this.description + "): " + this.start_date + " - " + this.end_date;
}


function RunningTask() {
    Task.apply(this, arguments);
    this.completed = false;
    this.state = 0;
}

RunningTask.prototype = Object.create(Task.prototype);
RunningTask.prototype.constructor = RunningTask;

RunningTask.prototype.complete = function() {
    this.completed = true;
    this.state = 100;
}


task = new RunningTask("Work", "Some work", Date(), Date(), [])
alert(task);
