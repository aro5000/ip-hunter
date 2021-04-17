package main

import (
	"encoding/json"
	"fmt"
	"net"
	"net/http"
	"os"
	"time"
)

type searcher struct {
	Target  string
	Count   int
	Results map[string]bool
}

type Payload struct {
	Answer []*PayloadData `json:"answer"`
}

type PayloadData struct {
	Data string `json:"data"`
	Type int    `json:"type"`
}

func (s *searcher) printResults() {
	fmt.Println("\nResults:")
	for k, _ := range s.Results {
		fmt.Println(k)
	}
}

func (s *searcher) uniqueResults(x map[string]bool) {
	for k, _ := range x {
		if !s.Results[k] {
			s.Results[k] = true
		}
	}
}

func (s *searcher) googledns(c chan map[string]bool) {
	req, _ := http.NewRequest("GET", "https://dns.google.com/resolve?name="+s.Target+"&type=A", nil)
	results := getDohIps(req, s.Count)
	c <- results
}

func (s *searcher) cloudflaredns(c chan map[string]bool) {
	req, _ := http.NewRequest("GET", "https://cloudflare-dns.com/dns-query?name="+s.Target+"&type=A", nil)
	req.Header.Set("accept", "application/dns-json")
	results := getDohIps(req, s.Count)
	c <- results
}

func (s *searcher) localresolver(c chan map[string]bool) {
	results := map[string]bool{}
	for i := 1; i <= s.Count; i++ {
		ips, err := net.LookupIP(s.Target)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Could not get IPs: %v\n", err)
			break
		}
		for _, v := range ips {
			// for now only get ipv4 addresses
			if len(v) == 4 {
				if !results[v.String()] {
					results[v.String()] = true
				}
			}
		}
	}
	c <- results
}

func getClient() http.Client {
	timeout := time.Duration(5 * time.Second)
	client := http.Client{
		Timeout: timeout,
	}
	return client
}

func getDohIps(req *http.Request, count int) map[string]bool {
	client := getClient()
	res := map[string]bool{}

	for i := 1; i <= count; i++ {
		resp, err := client.Do(req)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Failed HTTP request to %v\n", req.URL)
			break
		}
		var p Payload
		err = json.NewDecoder(resp.Body).Decode(&p)
		if err != nil {
			fmt.Fprintf(os.Stderr, "[!]Failed to decode DoH JSON results from %v\n", req.URL)
			break
		}
		// Loop through results and add to the map if the value doesn't already exist
		// Also check to ensure we are getting a "type 1" A record response
		for _, v := range p.Answer {
			if v.Type == 1 {
				if !res[v.Data] {
					res[v.Data] = true
				}
			}
		}
	}

	return res
}
