package main

import (
	"crypto/tls"
	"fmt"
	"io"
	"log"
	"net/http"
	"net/url"
	"os"
	"time"

	"github.com/corpix/uarand"
)

var (
	TL       string = "zh-CN"
	ProxyUrl string = "http://127.0.0.1:7890"
)

func TextToAudio(txt string) {
	txt = url.QueryEscape(txt)
	api := "https://translate.google.com/translate_tts?ie=UTF-8&client=zh-cn&tl=" + TL + "&q=" + txt
	proxy, _ := url.Parse(ProxyUrl)
	client := &http.Client{
		Timeout: 10 * time.Second,
		Transport: &http.Transport{
			Proxy:           http.ProxyURL(proxy),
			TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
		},
	}
	req, _ := http.NewRequest("GET", api, nil)
	req.Header.Set("User-Agent", uarand.GetRandom())
	resp, err := client.Do(req)
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()
	filename := txt + ".mp3"
	out, err := os.Create(filename)
	if err != nil {
		log.Fatal(err)
	}
	defer out.Close()
	io.Copy(out, resp.Body)
	fmt.Printf("完成： %s\n", filename)
}

func main() {
	// TextToAudio(os.Args[1])
	txt := os.Args[1]
	fmt.Printf("输入: %s\n", txt)
	TextToAudio(txt)
}
