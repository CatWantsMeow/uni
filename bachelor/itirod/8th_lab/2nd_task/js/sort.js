function parseInt(value) {
    var intValue = +value;
    if (isNaN(intValue)) {
        throw new Error(value + " is not a number");
    }
    return intValue;
}


function sort(array, comparer) {
    function qsort(l, r) {
        var i = l;
        var j = r;
        var m = array[Math.floor((i + j) / 2)];

        while (i <= j) {
            while (comparer(array[i], m) < 0) i++;
            while (comparer(array[j], m) > 0) j--;
            if (i <= j) {
                var temp = array[i];
                array[i] = array[j];
                array[j] = temp;
                i++;
                j--;
            }
        }

        if (i < r) qsort(i, r);
        if (j > l) qsort(l, j);
    }
    qsort(0, array.length);
}


try {
    count = parseInt(prompt("Введите количество элементов:"));
    array = [];
    for (var i = 0; i < count; i++) {
        var value = parseInt(prompt("Введите значение номер " + i));
        array.push(value);
    }

    comparer = function (a, b) { return a - b; }
    sort(array, comparer);
    alert(array);
}
catch (e) {
    alert(e.message);
}
