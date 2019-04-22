function numberCheck(func) {
    return (arg) =>  {
        if (typeof(param) != "number")
            throw Error(param + " is not a number");
        return func(param);
    }
}

function typeCheck(func, type) {
    return (...args) => {
        args.forEach((arg, i, args) => {
            if (typeof(arg) != type)
                throw new Error("Argument " + arg + " is not " + type)
        });
        return func(...args);
    }
}


function parseNumber(value) {
    var intValue = +value;
    if (isNaN(intValue)) {
        return value;
    }
    return intValue;
}


function avg(...numbers) {
    return numbers.reduce((sum, elem) => { return sum + elem / numbers.length }, 0)
}


values = [];
for (let i = 0; i < 5; i++) {
    value = parseNumber(prompt("Введите значение:"));
    values[i] = value;
}

try {
    typeCheckedAvg = typeCheck(avg, "number");
    alert(typeCheckedAvg(values[0], values[1], values[2], values[3], values[4]));
}
catch (e) {
    alert(e.message);
}
