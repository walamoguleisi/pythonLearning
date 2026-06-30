# 加入暂停播放和继续播放按钮

import tkinter as tk
import time
import threading

# 全局控制变量
is_pause = False
is_running = False

# 窗口初始化（放大窗口）
root = tk.Tk()
root.title("一年级数学：公交车人数倒推动画（带暂停控制）")
root.geometry("1200x750")  # 窗口放大
root.resizable(False, False)

# 画布放大
canvas = tk.Canvas(root, width=1200, height=620, bg="#f0f8ff")
canvas.pack()

# 字体定义
font_big = ("微软雅黑", 24, "bold")
font_mid = ("微软雅黑", 20)
font_small = ("微软雅黑", 16)

# 绘制公交车
def draw_bus():
    canvas.delete("bus")
    # 车身
    canvas.create_rectangle(100, 180, 1100, 440, fill="#4299e1", outline="black", width=4, tags="bus")
    # 车窗
    for i in range(7):
        x1 = 130 + i * 130
        canvas.create_rectangle(x1, 200, x1+110, 310, fill="white", outline="black", tags="bus")
    # 车轮
    canvas.create_oval(200, 430, 280, 510, fill="#333333", tags="bus")
    canvas.create_oval(920, 430, 1000, 510, fill="#333333", tags="bus")
    canvas.create_text(600, 130, text="公交车人数问题动画", font=("微软雅黑", 28, "bold"), fill="#2c5282", tags="bus")

# 清空人物、文字
def clear_all():
    canvas.delete("person")
    canvas.delete("text")
    root.update()

# 绘制小人
def draw_person(x, y, tag="person", color="#e53e3e"):
    canvas.create_oval(x, y, x+24, y+24, fill=color, tags=tag)
    canvas.create_line(x+12, y+24, x+12, y+52, fill=color, width=3, tags=tag)
    canvas.create_line(x, y+34, x+24, y+34, fill=color, width=3, tags=tag)
    canvas.create_line(x+12, y+52, x, y+66, fill=color, width=3, tags=tag)
    canvas.create_line(x+12, y+52, x+24, y+66, fill=color, width=3, tags=tag)

# 带暂停检测的延时
def sleep_check(sec):
    global is_pause
    t = 0
    step = 0.05
    while t < sec:
        while is_pause:
            root.update()
            time.sleep(0.05)
        time.sleep(step)
        t += step
        root.update()

# 动画主逻辑
def run_animation():
    global is_running, is_pause
    if is_running:
        return
    is_running = True
    btn_start.config(state=tk.DISABLED)
    btn_restart.config(state=tk.DISABLED)
    is_pause = False

    draw_bus()
    sleep_check(1)

    # 步骤1 出示题目
    clear_all()
    draw_bus()
    canvas.create_text(600, 80, text="题目：车上原来有一些人，到站下去5人，上来3人，现在车上13人，原来有几人？",
                       font=font_mid, fill="#1a202c", tags="text")
    sleep_check(3)
    clear_all()
    draw_bus()

    # 步骤2 现在13人
    canvas.create_text(600, 80, text="第一步：现在车上有13人", font=font_big, fill="#2b6cb0", tags="text")
    pos_x = 140
    for i in range(13):
        draw_person(pos_x, 220)
        pos_x += 52
        sleep_check(0.15)
    sleep_check(2)

    # 步骤3 减去上车3人
    canvas.create_text(600, 118, text="倒推1：把后来上车的3个人请下车（减去3）", font=font_mid, fill="#2f855a", tags="text")
    for i in range(3):
        draw_person(140 + 52*(10+i), 220, color="#38a169")
    sleep_check(2)
    canvas.delete("person")
    pos_x = 140
    for i in range(10):
        draw_person(pos_x, 220)
        pos_x += 52
    canvas.create_text(600, 540, text="算式：13 - 3 = 10", font=font_big, fill="green", tags="text")
    sleep_check(3)

    # 步骤4 加回下车5人
    canvas.delete("text")
    canvas.create_text(600, 80, text="倒推2：把之前下车的5个人接回来（加上5）", font=font_mid, fill="#c53030", tags="text")
    for i in range(5):
        draw_person(140 + 52*(10+i), 220, color="#e53e3e")
        sleep_check(0.3)
    canvas.create_text(600, 540, text="算式：10 + 5 = 15", font=font_big, fill="red", tags="text")
    sleep_check(3)

    # 汇总答案页面
    clear_all()
    draw_bus()
    canvas.create_text(600, 70, text="完整解题过程（倒推法）", font=font_big, fill="#742a2a", tags="text")
    canvas.create_text(600, 130, text="现在人数：13人", font=font_mid, tags="text")
    canvas.create_text(600, 170, text="先去掉上车的3人：13 - 3 = 10", font=font_mid, fill="green", tags="text")
    canvas.create_text(600, 210, text="再加回下车的5人：10 + 5 = 15", font=font_mid, fill="red", tags="text")
    canvas.create_text(600, 280, text="综合算式：13 - 3 + 5 = 15", font=("微软雅黑", 28, "bold"), fill="#2c5282", tags="text")
    canvas.create_text(600, 360, text="答：车上原来有15人", font=("微软雅黑", 30, "bold"), fill="#d69e2e", tags="text")

    pos_x = 130
    for i in range(15):
        draw_person(pos_x, 320)
        pos_x += 46
        sleep_check(0.1)
    sleep_check(3)
    canvas.create_text(600, 540, text="动画演示完成，可点击重新播放", font=font_small, fill="#4a5568", tags="text")

    is_running = False
    btn_start.config(state=tk.NORMAL)
    btn_restart.config(state=tk.NORMAL)

# 按钮控制函数
def toggle_pause():
    global is_pause
    is_pause = not is_pause
    if is_pause:
        btn_pause.config(text="继续播放")
    else:
        btn_pause.config(text="暂停动画")

def restart_anim():
    if is_running:
        return
    clear_all()
    draw_bus()
    threading.Thread(target=run_animation, daemon=True).start()

# 底部按钮区域
frame_ctrl = tk.Frame(root)
frame_ctrl.pack(pady=8)

btn_start = tk.Button(frame_ctrl, text="开始动画", font=font_small, bg="#63b3ed", width=12,
                      command=lambda: threading.Thread(target=run_animation, daemon=True).start())
btn_start.grid(row=0, column=0, padx=10)

btn_pause = tk.Button(frame_ctrl, text="暂停动画", font=font_small, bg="#f6e05e", width=12, command=toggle_pause)
btn_pause.grid(row=0, column=1, padx=10)

btn_restart = tk.Button(frame_ctrl, text="重新播放", font=font_small, bg="#68d391", width=12, command=restart_anim)
btn_restart.grid(row=0, column=2, padx=10)

draw_bus()
root.mainloop()
