function parseNumber(value) {
    var intValue = +value;
    if (isNaN(intValue)) {
        throw new Error("Неправильный формат данных: " + value);
    }
    return intValue;
}


function isRectangle(points) {
    firstCase = points[0].y == points[1].y;
    firstCase = firstCase && points[1].x == points[2].x;
    firstCase = firstCase && points[2].y == points[3].y;
    firstCase = firstCase && points[3].x == points[0].x;

    if (firstCase) {
        rect = [];
        rect[0] = points[0];
        rect[1] = points[2];
        return rect;
    }

    secondCase = points[0].x == points[1].x;
    secondCase = secondCase && points[1].y == points[2].y;
    secondCase = secondCase && points[2].x == points[3].x;
    secondCase = secondCase && points[3].y == points[0].y;

    if (secondCase) {
        rect = [];
        rect[0] = points[1];
        rect[1] = points[3];
        return rect;
    }

    return null;
}


function isIn(point, rect) {
    firstCase = rect[0].x <= point.x && point.x <= rect[1].x;
    firstCase = firstCase && rect[0].y <= point.y && point.y <= rect[1].y;

    secondCase = rect[1].x <= point.x && point.x <= rect[0].x;
    secondCase = secondCase && rect[1].y <= point.y && point.y <= rect[0].x;

    return firstCase || secondCase;
}


try {
    points = [{}, {}, {}, {}];
    for (var i = 0; i < points.length; i++) {
        points[i].x = parseNumber(prompt('Введите x' + (i + 1)));
        points[i].y = parseNumber(prompt('Введите y' + (i + 1)));
    }

    rect = isRectangle(points);
    if (!rect) throw new Error("Введенные точки не образуют прямоугольник");

    point = {};
    point.x = parseNumber(prompt('Введите x точки:'));
    point.y = parseNumber(prompt('Введите y точки:'));

    if (isIn(point, rect))
        alert("Точка внутри прямоугольника");
    else
        alert("Точка вне прямоугольника");
}
catch (e) {
    alert(e.message);
}
