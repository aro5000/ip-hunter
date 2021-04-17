FROM golang:1.15-alpine as build
WORKDIR /app
ADD cmd/ ./cmd
ENV GOPATH /go
ENV CGO_ENABLED=0
RUN go build ./cmd/ip-hunter

FROM alpine:latest
COPY --from=build /app/ip-hunter /app/
WORKDIR /app
RUN chown 65534:65534 ip-hunter
USER 65534:65534
ENTRYPOINT [ "./ip-hunter" ]
