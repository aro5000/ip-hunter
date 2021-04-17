# IP-HUNTER
This is now open sourced from a previous project I worked on. This may not help in all scenarios but has helped me before to get away from making a cheesy "dig/nslookup loop" script.

This tool will query various DNS servers in hopes of getting all IP's a particular domain resolves to.

It will query Google DNS, Cloudflare DNS, and whatever the local resolver is 4 times and remove any
duplicates. This is in hopes of triggering any round-robbin DNS resolver to get any possible IP a
domain resolves to.

## Rewrite!
To get more practice with golang, I decided to rewrite this tool from the original python. However, you will still be able to get the original python code held in the `python` branch of this repo. Comparing each version side by side and running against the same domain, I see on average ~60% performance increase from the go binary.

# Build/Run
The easiest way to run is with the container image:
```
docker run -it --rm registry.gitlab.com/aro5000/ip-hunter:latest domain.to.query.here
```

## Container
Use the following commands to build and run this tool as a container:
```
docker build -t iphunter .
docker run -it --rm iphunter <domain>
```

## Local
Use the following commands to build and run this tool locally (need golang installed):
```
go build ./cmd/ip-hunter/
./ip-hunter <domain>
```
