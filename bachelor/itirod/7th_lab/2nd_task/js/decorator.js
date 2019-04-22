function numberCheck(func) {
    return function(param) {
        if (typeof(param) != "number") {
            throw Error(param + " is not a number");
        }
        return func(param);
    }
}

function typeCheck(func, type) {
    return function() {
        for (var i = 0; i < arguments.length; i++) {
            if (typeof(arguments[i]) != type) {
                throw Error("Parameter " + arguments[i] + " is not " + type);
            }
        }
        return func.apply(null, arguments);
    }
}


function parseNumber(value) {
    var intValue = +value;
    if (isNaN(intValue)) {
        return value;
    }
    return intValue;
}


function avg() {
    var sum = 0;
    for (var i = 0; i < arguments.length; i++) {
        sum += arguments[i];
    }
    return sum / arguments.length;
}


values = [];
for (var i = 0; i < 5; i++) {
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
