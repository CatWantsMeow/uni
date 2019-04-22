function parseInt(value) {
    let intValue = +value;
    if (isNaN(intValue)) {
        throw new Error(value + " is not a number");
    }
    return intValue;
}


function range(start, stop, step) {
    values = [];
    if (start < stop) {
        for (let value = start; value <= stop; value += step) {
            values.push(value);
        }
    }
    else {
        for (let value = start; value >= stop; value += step) {
            values.push(value);
        }
    }
    return values;
}


try {
    start = parseInt(prompt("Введите начало последовательности:"));
    stop = parseInt(prompt("Введите конец последовательности:"));
    step = parseInt(prompt("Введите шаг последовательности:"));
    if (step == 0) throw new Error("Шаг не может быть равен 0");

    alert(range(start, stop, step));
}
catch (e) {
    alert(e.message);
}
