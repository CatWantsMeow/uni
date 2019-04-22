// file: vector/vector.go
package vector

import (
	"errors"
)

type (
	Vector    []float64
	Operation func(Vector, Vector) (Vector, error)
)

var Operations = map[string]Operation{
	"add": Add,
	"sub": Sub,
	"dot": Dot,
}

func checkLenghts(a Vector, b Vector) error {
	if len(a) != len(b) {
		return errors.New("vectors are different length")
	}
	return nil
}

func Add(a Vector, b Vector) (Vector, error) {
	if err := checkLenghts(a, b); err != nil {
		return nil, err
	}

	c := make(Vector, len(a), len(a))
	for i := 0; i < len(a); i++ {
		c[i] = a[i] + b[i]
	}
	return c, nil
}

func Sub(a Vector, b Vector) (Vector, error) {
	if err := checkLenghts(a, b); err != nil {
		return nil, err
	}

	c := make(Vector, len(a), len(a))
	for i := 0; i < len(a); i++ {
		c[i] = a[i] - b[i]
	}
	return c, nil
}

func Dot(a Vector, b Vector) (Vector, error) {
	if err := checkLenghts(a, b); err != nil {
		return nil, err
	}

	c := make(Vector, 1, 1)
	for i := 0; i < len(a); i++ {
		c[0] += a[i] * b[i]
	}
	return c, nil
}

func Perform(op string, a Vector, b Vector) (Vector, error) {
	opHandler, exists := Operations[op]
	if !exists {
		return nil, errors.New("operation is not supported")
	}
	return opHandler(a, b)
}
