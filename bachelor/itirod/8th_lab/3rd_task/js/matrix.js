function randomRange(min, max) {
    return Math.floor(Math.random() * (max - min) + min);
}


function createMatrix(n, m) {
    matrix = [];
    for (var i = 0; i < n; i++) {
        matrix[i] = [];
        for (var j = 0; j < m; j++) {
            matrix[i][j] = randomRange(0, 100);
        }
    }
    return matrix;
}


function matrixAddition(a, b) {
    if (a.length != b.length) {
        throw new Error("Размерности матриц не совпадают");
    }

    c = [];
    for (var i = 0; i < a.length; i++) {
        if (a[i].length != b[i].length) {
            throw new Error("Размерности матриц не совпадают")
        }

        c[i] = [];
        for (var j = 0; j < a[i].length; j++) {
            c[i][j] = a[i][j] + b[i][j];
        }
    }
    return c;
}


function printMatrix(a, elemId) {
    html = "<table cellpadding='10'>"
    for (var i = 0; i < a.length; i++) {
        html += "<tr>";
        for (var j = 0; j < a[i].length; j++) {
            html += "<td>" + a[i][j] + "</td>";
        }
        html += "</tr>";
    }
    html += "<table>";
    document.getElementById(elemId).innerHTML = html;
}


function parseInt(value) {
    var intValue = +value;
    if (isNaN(intValue)) {
        throw new Error(value + " is not a number");
    }
    return intValue;
}


try {
    n = parseInt(prompt("n = ", 5));
    m = parseInt(prompt("m = ", 5));

    a = createMatrix(n, m);
    b = createMatrix(n, m);
    c = matrixAddition(a, b);

    printMatrix(a, 'first_matrix');
    printMatrix(b, 'second_matrix');
    printMatrix(c, 'third_matrix');
}
catch (e) {
    alert(e.message);
}
