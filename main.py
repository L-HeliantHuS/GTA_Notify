import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import config
import socket
from threading import Thread
import json
import time
from pynput import keyboard
import winsound

is_running = False
sock = None
thread1 = None
thread2 = None
listener = None


def log(log):
    try:
        logs.insert("end", str(log) + "\n")
    except Exception as e:
        logs.insert("end", "连接断开!\n")
        logs.see(logs.END)


def disabled():
    global is_running

    is_running = True

    status_text.set("已连接")
    roomID.pack(side=ttk.LEFT, padx=0, pady=5)
    disConnectBtn.pack(side=ttk.RIGHT, padx=0, pady=3)
    connectBtn.pack_forget()
    roomID.config(state="disabled")
    connectBtn.config(state="disabled")

def enabled():
    global is_running
    is_running = False
    status_text.set("未连接")
    disConnectBtn.pack_forget()
    roomID.pack(side=ttk.LEFT, padx=0, pady=5)
    connectBtn.pack(side=ttk.RIGHT, padx=0, pady=3)
    roomID.config(state="normal")
    connectBtn.config(state="normal")


def disConnect():
    global is_running
    is_running = False
    sock.close()

    thread1.join()
    thread2.join()
    
    enabled()

    log("已退出所有线程")

    


def send(sock, message):
    print(json.dumps(message))
    try:
        sock.sendall(json.dumps(message).encode("utf-8"))
    except Exception as e:
        if sock == None:
            log("未连接，请在连接后按F5")

def receive(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                log("已断开连接")
                enabled()
                exit()

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



def on_press(key, sock):

    try:
        if key == keyboard.Key.f5:
            log('检测到按下f5')
            send(sock, {'type': 'notify', 'roomid': roomID.get()})
    except AttributeError:
        log("报错了")


def listen_keys():
    global sock, listener
    with keyboard.Listener(on_press=lambda key: on_press(key, sock)) as li:
        listener = li
        listener.join()


def connect():
    id = roomID.get()

    if id.strip() == "":
        log("ROOMID不能为空！")

    else:
        disabled()
        log(f"ROOMID为:{id}")
        global sock, thread1, thread2
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
            
        except:
            log("断开连接")
            enabled()


def init_config():
    # 初始化ROOMID
    roomID.insert(0, config.get_config("settings", "ROOMID"))


def on_closing():
    global listener
    disConnect()
    listener.stop()
    root.destroy()


root = ttk.Window(title="GTA_Notify 2.0",
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


roomID = ttk.Entry(roomIDFrame, width=30)
roomID.pack(side=ttk.LEFT, padx=0, pady=5)

test = ttk.Label(root, text="和小伙伴输入相同的ROOMID\n然后按下F5即可让相同ROOMID的朋友听到提示音\n\n            Author: -_Hel1antHu5_CrY")
test.pack(side=ttk.BOTTOM, padx=2, pady=5)



ttk.Label(root, text="实时日志", bootstyle=SUCCESS).place(x=3, y=115)
logs = ttk.Text(root, width=52, height=23, wrap="word")
logs.place(x=3, y=140)

root.protocol("WM_DELETE_WINDOW", on_closing)


if __name__ == "__main__":
    init_config()
    Thread(target=listen_keys).start()
    log("键盘监听已启动")
    log("""
    [NEWS]GTA Notify 2.0
        优化了创建连接的方式
        修复点击连接后按钮乱跑的问题
        修复了会多次创建键盘监听键盘事件，导致按键没反应的问题
""")
    log("等待连接……")
    root.mainloop()