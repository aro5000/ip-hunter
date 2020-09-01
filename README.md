# IP-HUTNER
This is now open sourced from a previous project I worked on. This may not help in all scenarios but has helped me before to get away from making a cheesy "dig/nslookup loop" script.

This tool will query various DNS servers in hopes of getting all IP's a particular domain resolves to.

It will query Google DNS, Cloudflare DNS, and whatever the local resolver is 4 times and remove any 
duplicates. This is in hopes of triggering any round-robbin DNS resolver to get any possible IP a 
domain resolves to.

# Build/Run
The easiest way to run is with the container image:
```
docker run -it --rm registry.gitlab.com/aro5000/ip-hunter:latest domain.to.query.here
```
Using python directly:
```
usage: main.py [-h] target

positional arguments:
  target      Enter the domain or subdomain you want to query

optional arguments:
  -h, --help  show this help message and exit
```
## Container
Use the following commands to build and run this tool as a container:
```
docker build -t iphunter .
docker run -it --rm iphunter <domain>
``` 

## Local
Use the following commands to build and run this tool locally:
```
cd src/
pip3 install -r requirements.txt
python3 main.py <domain>
```
