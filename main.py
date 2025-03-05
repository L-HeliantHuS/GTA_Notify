import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import config

def init_config():
    # 初始化卡单
    kd_hotkey_input.config(state="normal")
    kd_hotkey_input.insert(0, config.get_config("keys", "kd"))
    kd_hotkey_input.config(state="disabled")

    # 初始化卡单时间
    kd_time_input.config(state="normal")
    kd_time_input.insert(0, config.get_config("settings", "SUSPEND_TIME"))
    kd_time_input.config(state="disabled")

    # 初始化杀进程
    kill_gta_input.config(state="normal")
    kill_gta_input.insert(0, config.get_config("keys", "kill"))
    kill_gta_input.config(state="disabled")


root = ttk.Window(title="GTAOTools - 大鸟转转转酒吧洛圣都分鸟",
                  themename="superhero",
                  size=(800,600),
                  position=(800,300),
                  minsize=(100,200),
                  maxsize=(2560,1440))

# 运行状态， 默认未运行，需等待监听线程启动成功后修改
listen_status = ttk.Label(root, text="未运行", bootstyle=WARNING)
listen_status.place(y=0)

# 卡单相关
kd_label_frame = ttk.LabelFrame(text="卡单相关")
kd_label_frame.place(x=5,y=25, width=380, height=150)


kd1 = ttk.Frame(kd_label_frame)
kd1.place(x=0, y=0, width=350, height=60)

kd_hotkey_label = ttk.Label(kd1, text="卡单快捷键：", bootstyle=INFO)
kd_hotkey_label.pack(side=ttk.LEFT, padx=5, pady=5)

kd_hotkey_btn = ttk.Button(kd1, text="修改")
kd_hotkey_btn.pack(side=ttk.RIGHT, padx=0, pady=3)

kd_hotkey_input = ttk.Entry(kd1)
kd_hotkey_input.pack(side=ttk.RIGHT, padx=0, pady=5)
kd_hotkey_input.config(state="disabled")



kd2 = ttk.Frame(kd_label_frame)
kd2.place(x=0, y=60, width=350, height=60)

kd_time_label = ttk.Label(kd2, text="卡单时间：", bootstyle=INFO)
kd_time_label.pack(side=ttk.LEFT, padx=5, pady=5)

kd_time_btn = ttk.Button(kd2, text="修改")
kd_time_btn.pack(side=ttk.RIGHT, padx=0, pady=3)

kd_time_input = ttk.Entry(kd2)
kd_time_input.pack(side=ttk.RIGHT, padx=0, pady=5)
kd_time_input.config(state="disabled")




# 杀进程相关
kill_gta_label_frame = ttk.LabelFrame(text="杀进程相关")
kill_gta_label_frame.place(x=5,y=190, width=380, height=90)

k1 = ttk.Frame(kill_gta_label_frame)
k1.place(x=0, y=0, width=350, height=60)

kill_gta_label = ttk.Label(k1, text="杀进程快捷键：", bootstyle=INFO)
kill_gta_label.pack(side=ttk.LEFT, padx=5, pady=5)


kill_gta_btn = ttk.Button(k1, text="修改")
kill_gta_btn.pack(side=ttk.RIGHT, padx=0, pady=3)

kill_gta_input = ttk.Entry(k1)
kill_gta_input.pack(side=ttk.RIGHT, padx=0, pady=5)
kill_gta_input.config(state="disabled")



if __name__ == "__main__":
    init_config()
    root.mainloop()