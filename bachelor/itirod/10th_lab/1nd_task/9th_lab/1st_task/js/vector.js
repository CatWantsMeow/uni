class Vector {
    constructor(x, y, z) {
        this.x = x;
        this.y = y;
        this.z = z;
    }

    add(other) {
        this.x += other.x;
        this.y += other.y;
        this.z += other.z;
    }

    dot(other) {
        return this.x * other.x + this.y * other.y + this.z * other.z;
    }

    toString() {
        return "(" + this.x + ", " + this.y + ", " + this.z + ")";
    }

    valueOf(string) {
        return Math.sqrt(this.x * this.x + this.y * this.y + this.z * this.z)
    }

    print(elemId) {
        document.getElementById(elemId).innerHTML = this.toString();
    }

    get length() { return 3; }
}


let randomRange = (min, max) => {
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

first_vector.add(second_vector);
vector_dot = third_vector.dot(fourth_vector);

first_vector.print("vector_sum");
document.getElementById("vector_dot").innerHTML = vector_dot;
