package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"net"
	"sync"
	"time"
)

// 客户端结构体
type Client struct {
	conn      net.Conn
	roomID    string
	lastPing  time.Time
	sendMutex sync.Mutex
}

// 服务器管理的客户端集合
var clients = make(map[net.Conn]*Client)
var clientsMutex sync.Mutex

const HEARTBEAT_TIMEOUT = 60 * time.Second

func main() {
	// 监听 12345 端口
	listener, err := net.Listen("tcp", ":12345")
	if err != nil {
		fmt.Println("[错误] 监听失败:", err)
		return
	}
	defer listener.Close()
	fmt.Println("[服务器] 运行中，监听端口 12345...")

	// 启动定时任务，检查心跳
	go checkHeartbeats()

	for {
		conn, err := listener.Accept()
		if err != nil {
			fmt.Println("[错误] 连接失败:", err)
			continue
		}
		fmt.Println("[新连接] 客户端:", conn.RemoteAddr())

		// 创建客户端并存入 map
		client := &Client{conn: conn, lastPing: time.Now()}
		clientsMutex.Lock()
		clients[conn] = client
		clientsMutex.Unlock()

		// 启动新协程处理客户端消息
		go handleClient(client)
	}
}

// 处理客户端消息
func handleClient(client *Client) {
	conn := client.conn
	defer func() {
		conn.Close()
		clientsMutex.Lock()
		delete(clients, conn)
		clientsMutex.Unlock()
		fmt.Println("[断开] 客户端:", conn.RemoteAddr())
	}()

	reader := bufio.NewReader(conn)
	for {
		// 读取客户端消息
		message, err := reader.ReadString('}')
		if err != nil {
			fmt.Println("[错误] 读取消息失败:", err)
			return
		}

		// 解析 JSON
		var data map[string]string
		err = json.Unmarshal([]byte(message), &data)
		if err != nil {
			fmt.Println("[错误] JSON 解析失败:", err)
			continue
		}

		// 处理不同类型的消息
		switch data["type"] {
		case "init":
			client.roomID = data["roomid"]
			fmt.Println("[初始化] 客户端", conn.RemoteAddr(), "加入房间", client.roomID)

		case "heartbeat":
			client.lastPing = time.Now()
			fmt.Println("[心跳] 来自", conn.RemoteAddr())

		case "notify":
			fmt.Println("[通知] 房间", client.roomID, "收到 notify 消息")
			broadcast(client.roomID, "{'type': 'notify'}")

		default:
			fmt.Println("[未知消息] 来自", conn.RemoteAddr(), "内容:", data)
		}
	}
}

// 发送消息给特定 roomid 的客户端
func broadcast(roomID, message string) {
	clientsMutex.Lock()
	defer clientsMutex.Unlock()
	for _, client := range clients {
		if client.roomID == roomID {
			client.sendMutex.Lock()
			client.conn.Write([]byte(message + "\n"))
			client.sendMutex.Unlock()
		}
	}
}

// 定期检查心跳
func checkHeartbeats() {
	for {
		time.Sleep(5 * time.Second)
		now := time.Now()
		clientsMutex.Lock()
		for conn, client := range clients {
			if now.Sub(client.lastPing) > HEARTBEAT_TIMEOUT {
				fmt.Println("[超时] 客户端", conn.RemoteAddr(), "心跳超时，断开连接")
				conn.Close()
				delete(clients, conn)
			}
		}
		clientsMutex.Unlock()
	}
}
