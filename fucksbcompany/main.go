package main

import (
	"math/rand"
	"time"
)

// 生成随机时间间隔进行休眠
func sleepRandom() {
	maxInterval := 10 // 最大休眠间隔，单位：秒
	rand.Seed(time.Now().UnixNano())
	interval := rand.Intn(maxInterval)
	time.Sleep(time.Duration(interval) * time.Second)
}

func main() {
	var data [][]byte
	for {
		// 生成随机大小的字节数组，模拟数据
		n := rand.Intn(1000000)
		bytes := make([]byte, n)
		data = append(data, bytes)
		// 等待随机时间间隔
		sleepRandom()
	}
}
