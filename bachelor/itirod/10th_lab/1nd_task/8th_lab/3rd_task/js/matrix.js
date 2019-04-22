function randomRange(min, max) {
    return Math.floor(Math.random() * (max - min) + min);
}


function createMatrix(n, m) {
    matrix = [];
    for (let i = 0; i < n; i++) {
        matrix[i] = [];
        for (let j = 0; j < m; j++) {
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
    for (let i = 0; i < a.length; i++) {
        if (a[i].length != b[i].length) {
            throw new Error("Размерности матриц не совпадают")
        }

        c[i] = [];
        for (let j = 0; j < a[i].length; j++) {
            c[i][j] = a[i][j] + b[i][j];
        }
    }
    return c;
}


function printMatrix(a, elemId) {
    html = "<table cellpadding='10'>"
    a.forEach((row, i, a) => {
        html += "<tr>";
        row.forEach((elem, i, row) => {
            html += "<td>" + elem + "</td>";
        })
        html += "</tr>";
    })
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
