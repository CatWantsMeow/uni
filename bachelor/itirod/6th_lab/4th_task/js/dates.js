function parseNumber(value) {
    var intValue = +value;
    if (isNaN(intValue)) {
        throw new Error("Неправильный формат данных: " + value);
    }
    return intValue;
}


function days_count(year, month) {
    counts = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if (year % 4 == 0 && year % 400 != 0) counts[1]++;
    return counts[month - 1];
}


function day_of_week(year, month, day) {
    days_of_week = [
        "Четверг",
        "Пятница",
        "Суббота",
        "Воскресение",
        "Понедельник",
        "Вторник",
        "Среда",
    ];

    days = 0;
    for (var i = 2015; i < year; i++) {
        days_in_year = (i % 4 == 0 && i % 400 != 0) ? 366 : 365;
        days += days_in_year;
    }
    for (var i = 1; i < month; i++) {
        days += days_count(year, i);
    }
    days += day - 1;

    return days_of_week[days % 7];
}


try {
    year = parseNumber(prompt("Введите номер года:"));
    if (year < 0)
        throw new Error("Год должен быть нашей эры");

    month = parseNumber(prompt("Введите номер месяца (1..12):"));
    if (month < 1 && month > 12)
        throw new Error("Номер месяца должен быть в пределах от 1 до 12");

    day = parseNumber(prompt("Введите число в указанном месяце"));
    if (day < 1 && day > days_count(year, month))
        throw new Error("Число должно быть в пределах от 1 до " + days_count(month));

    alert(day_of_week(year, month, day));
}
catch (error) {
    alert(error.message);
}
