// file: api/handlers.go
package api

import (
	"encoding/json"
	"errors"
	"github.com/CatWantsMeow/vectorApp/app/vector"
	"net/http"
)

type RequestPayload struct {
	A  vector.Vector `json:"a"`
	B  vector.Vector `json:"b"`
	Op string        `json:"op"`
}

type ResponsePayload struct {
	Result vector.Vector `json:"result,omitempty"`
	Error  string        `json:"error,omitempty"`
}

func writeError(err error, w http.ResponseWriter) {
	w.WriteHeader(400)
	rsp := ResponsePayload{Error: err.Error()}
	json.NewEncoder(w).Encode(&rsp)
}

func validatePayload(payload RequestPayload) error {
	if payload.Op == "" {
		return errors.New("'op' parameter is required")
	}
	if payload.A == nil || len(payload.A) == 0 {
		return errors.New("'a' parameter is required")
	}
	if payload.B == nil || len(payload.B) == 0 {
		return errors.New("'b' parameter is required")
	}
	return nil
}

func CalculateHandler(w http.ResponseWriter, r *http.Request) {
	req := RequestPayload{}

	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeError(errors.New("failed to decode request JSON"), w)
		return
	}

	if err := validatePayload(req); err != nil {
		writeError(err, w)
		return
	}

	result, err := vector.Perform(req.Op, req.A, req.B)
	if err != nil {
		writeError(err, w)
		return
	}

	rsp := ResponsePayload{Result: result}
	json.NewEncoder(w).Encode(&rsp)
}

func HealthCheckHandler(w http.ResponseWriter, r *http.Request) {}
