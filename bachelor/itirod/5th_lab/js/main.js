window.onload = function() {
    document.getElementById("fold_button").onclick = function() {
        for (var i = 1; i < 7; i++) {
            document.getElementById("face_" + i).style.animationPlayState = "running";
            this.style.opacity = "0.3";
        }
    };

    document.getElementById("rotate_button").onclick = function() {
        document.getElementById("cube").style.animationPlayState = "running";
        this.style.opacity = "0.3";
    };
};
