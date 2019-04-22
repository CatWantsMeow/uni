function parseNumber(value) {
    var intValue = +value;
    if (isNaN(intValue)) {
        throw new Error("Неправильный формат данных: " + value);
    }
    return intValue;
}

function checkNumber(value) {
    if (value <= 0) {
        throw new Error("Число должно быть положительным: " + value);
    }
    return value;
}

try {
    floor_count = checkNumber(parseNumber(prompt("Введите количество этажей:")));
    porch_count = checkNumber(parseNumber(prompt("Введите число подъездов:")));
    apartment_count = checkNumber(parseNumber(prompt("Введите число квартир на этаже:")));
    apartment_number = checkNumber(parseNumber(prompt("Введите номер квартиры:")));
}
catch (error) {
    alert(error.message);
}

apartments_per_porch = floor_count * apartment_count
porch_number = Math.floor(apartment_number / apartments_per_porch)
if (apartment_number % apartments_per_porch > 0) porch_number++;

if (porch_number > porch_count) {
    alert("Квартиры с таким номером в доме нет");
}
else {
    alert("Указанная квартира в подъезде номер " + porch_number);
}
