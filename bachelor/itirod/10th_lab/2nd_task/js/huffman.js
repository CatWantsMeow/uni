class Node {
    constructor() {
        this.left = null;
        this.right = null;
        this.prob = null;
        this.value = null;
        this.code = "";
        this.parent = null;
        this.visited = false;
    }
}


function getCodes(prob) {
	let tree = new Array();
	let secondTree = new Array();

	this.getNext = () => {
    	if (tree.length > 0 && secondTree.length > 0 && tree[0].prob < secondTree[0].prob)
    	   return tree.shift();
    	if (tree.length > 0 && secondTree.length > 0 && tree[0].prob > secondTree[0].prob)
    	   return secondTree.shift();
    	if (tree.length > 0)
    	   return tree.shift();
    	return secondTree.shift();
	}
	let sortedProb = new Array();
	let codes = new Array();

	let x = 0;
	for (let elem in prob) {
        sortedProb[x] = new Array(elem, prob[elem]);
        x = x + 1;
	}

	sortedProb = sortedProb.sort((a, b) => { return a[1] - b[1] });

    x = 0;
	for (var elem in sortedProb) {
        tree[x] = new Node();
        tree[x].prob = sortedProb[elem][1];
        tree[x].value = sortedProb[elem][0];
        x = x + 1;
	}

	while (tree.length + secondTree.length > 1) {
		let left = getNext();
		let right = getNext();
		let newnode = new Node();
		newnode.left = left;
		newnode.right = right;
		newnode.prob = left.prob + right.prob;
		newnode.left.parent = newnode;
		newnode.right.parent = newnode;
		secondTree.push(newnode);
	}

	var currentnode = secondTree[0];
	var code = "";
	while (currentnode) {
		if (currentnode.value) {
			codes[currentnode.value] = code;
			code = code.substr(0, code.length - 1);
			currentnode.visited = true;
			currentnode = currentnode.parent;
		}
		else if (!currentnode.left.visited) {
			currentnode = currentnode.left;
			code += "0";
		}
		else if (!currentnode.right.visited) {
			currentnode = currentnode.right;
			code += "1";
		}
		else {
			currentnode.visited = true;
			currentnode = currentnode.parent;
			code = code.substr(0, code.length - 1);
		}
	}
	return codes;
}


function compressHuffman(input, codes) {
    let output = input.split("");
    for (let elem in output) {
      output[elem] = codes[output[elem]];
    }
    return output.join("");
}

function getProbabilities(input) {
  let prob = new Array();
  let x = 0;
  let len = input.length;
  while (x < len) {
	  var chr = input.charAt(x);
	  if (prob[chr]) {
		  prob[chr] = prob[chr] + 1;
	  }
	  else {
		  prob[chr] = 1;
	  }
	  x++;
  }

  for (var elem in prob) {
	  prob[elem] = prob[elem] / len;
  }
  return prob;
}


window.onload = function() {
    let button = document.getElementById("compress")
    button.onclick = function() {
        var input = document.getElementById("input").value;
    	document.getElementById("inputlength").innerHTML = input.length * 8;

    	var probabilities = getProbabilities(input);
    	var codes = getCodes(probabilities);
    	var output = compressHuffman(input, codes);

        temp = "";
    	for (var elem in codes) {
    	  temp += elem + " = " + codes[elem] + "<br/>";
    	}

        document.getElementById("codes").innerHTML = temp;
    	document.getElementById("output").value = output;
    	document.getElementById("outputlength").innerHTML = output.length;
    }
}
