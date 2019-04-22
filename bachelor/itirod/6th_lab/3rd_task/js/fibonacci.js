function parseInt(value) {
    var intValue = +value;
    if (isNaN(intValue)) {
        throw new Error("Неправильный формат данных: " + value);
    }
    return intValue;
}


function Fibonacci(n) {
    var a = 1;
    var b = 1;
    for (var i = 0; i < n - 1; i++) {
        var c = b;
        b = a + b;
        a = c;
    }
    return a;
}


var n = prompt();
try {
    n = parseInt(n);
    if (n > 100) {
        throw new Error("Слишком большое значение: " + n);
    }
    alert(Fibonacci(n));
}
catch(e) {
    alert(e.message);
}
