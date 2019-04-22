// file: app.go
package main

import (
	"github.com/CatWantsMeow/vectorApp/app/api"
	"log"
	"net/http"
)

func main() {
	http.HandleFunc("/vector/", api.CalculateHandler)
	http.HandleFunc("/", api.HealthCheckHandler)
	log.Fatal(http.ListenAndServe(":8080", nil))
}
