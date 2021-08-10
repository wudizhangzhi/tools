package main

import (
	"fmt"
	"io/fs"
	"log"
	"os"
	"path/filepath"
	"runtime"
	"syscall"
	"time"
)

var (
	srcDir string
	dstDir string
)

// 获取创建时间
func GetFileCreateTime(path string) int64 {
	osType := runtime.GOOS
	fileInfo, _ := os.Stat(path)
	if osType == "windows" {
		wFileSys := fileInfo.Sys().(*syscall.Win32FileAttributeData)
		tNanSeconds := wFileSys.CreationTime.Nanoseconds() /// 返回的是纳秒
		tSec := tNanSeconds / 1e9                          ///秒
		return tSec
	}
	return time.Now().Unix()
}

// 时间戳转化为字符串
func unixToStr(t int64, f string) string {
	if f == "" {
		f = "2006-01-02 15:04:05"
	}
	return time.Unix(t, 0).Format(f)
}

func Exists(path string) bool {
	_, err := os.Stat(path) //os.Stat获取文件信息
	if err != nil {
		return os.IsExist(err)
	}
	return true
}

func main() {
	fmt.Println("请输入源目录路径:")
	fmt.Scanln(&srcDir)
	fmt.Println("请输目标路径:")
	fmt.Scanln(&dstDir)
	count := 0
	filepath.WalkDir(srcDir, func(p string, d fs.DirEntry, err error) error {
		if d.Type().IsRegular() {
			createTime := GetFileCreateTime(p)
			createTimeMonthStr := unixToStr(createTime, "2006-01")
			td := filepath.Join(dstDir, createTimeMonthStr)
			if !Exists(td) {
				os.Mkdir(td, 0666)
			}
			filename := filepath.Base(p)
			newPath := filepath.Join(dstDir, createTimeMonthStr, filename)
			err := os.Rename(p, newPath)
			if err != nil {
				log.Panic(err)
			}
			count++
			fmt.Printf("整理 %d个文件\r", count)
		}
		return nil
	})
}
