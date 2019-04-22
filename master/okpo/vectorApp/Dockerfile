FROM golang

COPY ./app /go/src/github.com/CatWantsMeow/vectorApp/app/
WORKDIR /go/src/github.com/CatWantsMeow/vectorApp/app/
RUN CGO_ENABLED=0 GOOS=linux go build . && \
    mkdir -p /go/bin && \
    mv -v app /go/bin/

FROM alpine
COPY --from=0 /go/bin/app /app
CMD ["/app"]
