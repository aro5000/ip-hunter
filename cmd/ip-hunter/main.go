package main

import (
	"fmt"
	"os"
)

func main() {
	var s searcher
	s.Results = map[string]bool{}
	s.Count = 4
	if len(os.Args) > 1 {
		s.Target = os.Args[1]
		fmt.Println("Target:", s.Target)
	} else {
		panic("[!] No target provided")
	}

	c := make(chan map[string]bool, 3)
	go s.googledns(c)
	go s.cloudflaredns(c)
	go s.localresolver(c)

	s.uniqueResults(<-c)
	s.uniqueResults(<-c)
	s.uniqueResults(<-c)
	s.printResults()
}
