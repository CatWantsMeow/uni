function parseNumber(value) {
    var intValue = +value;
    if (isNaN(intValue)) {
        throw new Error("Неправильный формат данных: " + value);
    }
    return intValue;
}


function compareNumbers(first, second) {
    if (first == second) {
        alert("Числа равны");
    }
    else if (first > second) {
        alert("Первое число больше второго");
    }
    else {
        alert("Второе число больше первого");
    }
}


while (true) {
    try {
        first_number = parseNumber(prompt("Первое число:"));
        second_number = parseNumber(prompt("Второе число:"));
        compareNumbers(first_number, second_number);
    }
    catch (error) {
        alert(error.message);
        break;
    }
}
