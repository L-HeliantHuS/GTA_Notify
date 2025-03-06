import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import config
import socket
from threading import Thread
import json
import time
import keyboard
import winsound

sock = None

is_running = False

thread1 = None
thread2 = None
thread3 = None


def log(log):
    try:
        logs.insert("end",log + "\n")
    except:
        logs.insert("end", "连接断开!")
        logs.see(ttk.END)


def disabled():
    global is_running

    is_running = True

    status_text.set("已连接")
    
    disConnectBtn.pack(side=ttk.RIGHT, padx=0, pady=3)
    connectBtn.pack_forget()
    roomID.config(state="disabled")
    connectBtn.config(state="disabled")

def enabled():
    global is_running
    is_running = False
    status_text.set("未连接")
    disConnectBtn.pack_forget()
    connectBtn.pack(side=ttk.RIGHT, padx=0, pady=3)
    roomID.config(state="normal")
    connectBtn.config(state="normal")


def disConnect():
    global is_running
    is_running = False
    sock.close()
    keyboard.unhook_all()

    thread1.join()
    thread2.join()
    
    enabled()

    log("已退出所有线程")

    


def send(sock, message):
    print(json.dumps(message))
    try:
        sock.sendall(json.dumps(message).encode("utf-8"))
    except:
        log(message)

def receive(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                log("已断开连接")
                enabled()
                break

            data = data.decode().replace("'", '"')
            msg = json.loads(data)
            
            if msg['type'] == 'heartbeat':
                log("与服务器通讯正常……")
            
            elif msg['type'] == 'notify':
                # 播放一段音频
                log('收到notify')
                winsound.PlaySound("success.wav", winsound.SND_FILENAME|winsound.SND_ASYNC)

        except:
            # enabled()
            break
    

def heartbeat(sock, id):
    while True:
        if is_running == False:
            break
        send(sock, {'type': 'heartbeat', 'roomid': id})
        time.sleep(3)


def listen_keys(sock, id):
    while True:
        if is_running == False:
            break
        keyboard.wait(config.get_config("keys", "key"))
        send(sock, {'type': 'notify', 'roomid': id})





def connect():
    disabled()
    id = roomID.get()
    
    log(f"ROOMID为:{id}")
    global sock, thread1, thread2, thread3
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((config.get_config("settings", "SERVER_IP"), int(config.get_config("settings", "SERVER_PORT"))))

        
        # 初始化
        send(sock, {'type': 'init', 'roomid': id})
        log("初始化连接中……")


        thread1 = Thread(target=receive, args=(sock,))
        thread1.start()
        log("消息接收已启动")

        thread2 = Thread(target=heartbeat, args=(sock,id))
        thread2.start()
        log("心跳检测已启动")

        thread3 = Thread(target=listen_keys, args=(sock,id))
        thread3.start()
        log("键盘监听已启动")

    except:
        log("断开连接")
        enabled()



def init_config():
    # 初始化ROOMID
    roomID.insert(0, config.get_config("settings", "ROOMID"))

root = ttk.Window(title="GTA_Notify | enjoy it!",
                  themename="superhero",
                  size=(390,665),
                  position=(800,300))

# 按键监听线程状态显示
listener_status = False
listener_thread = None
status_text = ttk.StringVar(root, value="未连接")

status_label = ttk.Label(root, textvariable=status_text, bootstyle=WARNING)
status_label.place(x=0, y=0, width=50, height=20)

roomIDFrameLabel = ttk.LabelFrame(text="房间信息")
roomIDFrameLabel.place(x=5,y=25, width=380, height=80)

roomIDFrame = ttk.Frame(roomIDFrameLabel)
roomIDFrame.place(x=0, y=0, width=350, height=50)

roomIDLabel = ttk.Label(roomIDFrame, text="ROOM ID: ", bootstyle=INFO)
roomIDLabel.pack(side=ttk.LEFT, padx=5, pady=5)

connectBtn = ttk.Button(roomIDFrame, text="连接", command=connect, bootstyle=SUCCESS)
connectBtn.pack(side=ttk.RIGHT, padx=0, pady=3)

disConnectBtn = ttk.Button(roomIDFrame, text="断开", command=disConnect, bootstyle=DANGER)


roomID = ttk.Entry(roomIDFrame)
roomID.pack(side=ttk.RIGHT, padx=0, pady=5)

test = ttk.Label(root, text="和小伙伴输入相同的ROOMID\n然后按下F5即可让相同ROOMID的朋友听到提示音")
test.pack(side=ttk.BOTTOM, padx=2, pady=5)



ttk.Label(root, text="实时日志", bootstyle=SUCCESS).place(x=3, y=115)
logs = ttk.Text(root, width=41, height=23, wrap="word")
logs.place(x=3, y=140)



if __name__ == "__main__":
    init_config()
    log("等待连接……")
    root.mainloop()