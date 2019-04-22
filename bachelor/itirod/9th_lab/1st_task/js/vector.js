function Vector(x, y, z) {
    this.x = x;
    this.y = y;
    this.z = z;
}

Vector.prototype.add = function addition(other) {
    return new Vector(this.x + other.x, this.y + other.y, this.z + other.z);
}

Vector.prototype.dot = function dotMultiplication(other) {
    return this.x * other.x + this.y * other.y + this.z * other.z;
}

Vector.prototype.toString = function vectorToString() {
    return "(" + this.x + ", " + this.y + ", " + this.z + ")";
}

Vector.prototype.valueOf = function vectorNorm(string) {
    return Math.sqrt(this.x * this.x + this.y * this.y + this.z * this.z)
}

Vector.prototype.print = function print(elemId) {
    document.getElementById(elemId).innerHTML = this.toString();
}

Object.defineProperties(Vector.prototype, {
    "length": {
        "get": function() { return 3; }
    }
});


function randomRange(min, max) {
    return Math.floor(Math.random() * (max - min) + min);
}


first_vector = new Vector(randomRange(0, 100), randomRange(0, 100), randomRange(0, 100));
second_vector = new Vector(randomRange(0, 100), randomRange(0, 100), randomRange(0, 100));
third_vector = new Vector(randomRange(0, 100), randomRange(0, 100), randomRange(0, 100));
fourth_vector = new Vector(randomRange(0, 100), randomRange(0, 100), randomRange(0, 100));

first_vector.print("first_vector");
second_vector.print("second_vector");
third_vector.print("third_vector");
fourth_vector.print("fourth_vector");

vector_sum = first_vector.add(second_vector);
vector_dot = third_vector.dot(fourth_vector);

vector_sum.print("vector_sum");
document.getElementById("vector_dot").innerHTML = vector_dot;
