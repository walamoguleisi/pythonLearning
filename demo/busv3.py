import tkinter as tk
import time
import threading

# 全局动画控制标记
is_pause = False
is_running = False

# 主窗口：1400宽，850高，保留大画面
root = tk.Tk()
root.title("一年级数学公交车人数应用题动画")
root.geometry("1400x850")
root.resizable(False, False)

# 画布
canvas = tk.Canvas(root, width=1400, height=720, bg="#f0f8ff")
canvas.pack()

# 字体：综合算式再缩小，答案醒目但不超大
font_title = ("微软雅黑", 28, "bold")
font_step = ("微软雅黑", 20)
font_formula = ("微软雅黑", 20, "bold")
font_answer = ("微软雅黑", 24, "bold")
font_btn = ("微软雅黑", 16)

# 绘制公交车：汇总页时位置会更低，避免压住答案
def draw_bus(y_offset=0):
    canvas.delete("bus")
    canvas.create_rectangle(60, 260 + y_offset, 1340, 500 + y_offset, fill="#4299e1", outline="black", width=4, tags="bus")

    for i in range(9):
        x1 = 100 + i * 138
        canvas.create_rectangle(x1, 280 + y_offset, x1+118, 350 + y_offset, fill="white", outline="black", tags="bus")

    canvas.create_oval(210, 490 + y_offset, 290, 560 + y_offset, fill="#222222", tags="bus")
    canvas.create_oval(1110, 490 + y_offset, 1190, 560 + y_offset, fill="#222222", tags="bus")

    canvas.create_text(700, 210 + y_offset, text="公交车人数解题动画", font=font_title, fill="#2c5282", tags="bus")

# 仅清空文字
def clear_text():
    canvas.delete("text")
    root.update()

# 仅清空小人
def clear_person():
    canvas.delete("person")
    root.update()

# 清空文字和小人，保留公交车
def clear_all_scene():
    clear_text()
    clear_person()

# 绘制小人：默认红色，后上车标记橙色
def draw_person(x, y, color="#e53e3e"):
    canvas.create_oval(x, y, x+22, y+22, fill=color, tags="person")
    canvas.create_line(x+11, y+22, x+11, y+48, fill=color, width=3, tags="person")
    canvas.create_line(x, y+32, x+22, y+32, fill=color, width=3, tags="person")
    canvas.create_line(x+11, y+48, x, y+62, fill=color, width=3, tags="person")
    canvas.create_line(x+11, y+48, x+22, y+62, fill=color, width=3, tags="person")

# 带暂停检测的延时
def sleep_check(sec):
    global is_pause
    step = 0.05
    total = 0
    while total < sec:
        while is_pause:
            root.update()
            time.sleep(0.05)
        time.sleep(step)
        total += step
        root.update()

# 动画主流程
def run_animation():
    global is_running, is_pause
    if is_running:
        return
    is_running = True
    btn_start.config(state=tk.DISABLED)
    btn_restart.config(state=tk.DISABLED)
    is_pause = False
    btn_pause.config(text="暂停动画")

    draw_bus()
    sleep_check(1)

    # ========== 步骤1 题目 ==========
    clear_all_scene()
    draw_bus()
    canvas.create_text(700, 60, text="题目：车上原来有一些人，到站下去5人，上来3人，现在车上13人，原来有几人？",
                       font=font_step, fill="#1a202c", tags="text")
    sleep_check(3)

    # ========== 步骤2 现在13人 ==========
    clear_all_scene()
    draw_bus()
    canvas.create_text(700, 60, text="第一步：现在车上一共有13人", font=font_step, fill="#2b6cb0", tags="text")

    pos_x = 120
    for i in range(13):
        draw_person(pos_x, 360)
        pos_x += 56
        sleep_check(0.15)
    sleep_check(2)

    # ========== 步骤3 倒推减3人 ==========
    clear_text()
    canvas.create_text(700, 60, text="倒推第一步：把后上车的3人请下车，减去3", font=font_step, fill="#2f855a", tags="text")

    for i in range(3):
        draw_person(120 + 56 * (10 + i), 360, color="#f59e0b")
    sleep_check(2)

    clear_person()
    pos_x = 120
    for i in range(10):
        draw_person(pos_x, 360)
        pos_x += 56

    canvas.create_text(700, 620, text="算式：13 - 3 = 10", font=font_formula, fill="green", tags="text")
    sleep_check(3)

    # ========== 步骤4 倒推加5人 ==========
    clear_text()
    canvas.create_text(700, 60, text="倒推第二步：把之前下车的5人接回来，加上5", font=font_step, fill="#c53030", tags="text")

    for i in range(5):
        draw_person(120 + 56 * (10 + i), 360, color="#e53e3e")
        sleep_check(0.3)

    canvas.create_text(700, 620, text="算式：10 + 5 = 15", font=font_formula, fill="red", tags="text")
    sleep_check(3)

    # ========== 汇总页面：重点修复重叠 ==========
    clear_all_scene()

    # 公交车下移80像素，避免压住答案
    draw_bus(y_offset=80)

    # 顶部解题过程，行距固定，不再堆叠
    canvas.create_text(700, 40, text="完整倒推解题过程", font=font_title, fill="#742a2a", tags="text")
    canvas.create_text(700, 85, text="1. 当前车上人数：13人", font=font_step, tags="text")
    canvas.create_text(700, 120, text="2. 去掉后上车3人：13 - 3 = 10", font=font_step, fill="#2f855a", tags="text")
    canvas.create_text(700, 155, text="3. 加回下车的5人：10 + 5 = 15", font=font_step, fill="#c53030", tags="text")

    # 综合算式上移，字号缩小
    canvas.create_text(700, 195, text="综合算式：13 - 3 + 5 = 15", font=font_formula, fill="#2c5282", tags="text")

    # 答案单独放在更上方，不再和车身重叠
    canvas.create_text(700, 245, text="答：车上原来有15人", font=font_answer, fill="#d69e2e", tags="text")

    # 原来15人展示：跟随公交车下移
    pos_x = 110
    for i in range(15):
        draw_person(pos_x, 360 + 80)
        pos_x += 50
        sleep_check(0.1)

    canvas.create_text(700, 620, text="动画演示完成，点击重新播放可从头观看", font=font_step, fill="#4a5568", tags="text")
    sleep_check(3)

    is_running = False
    btn_start.config(state=tk.NORMAL)
    btn_restart.config(state=tk.NORMAL)

# 暂停/继续
def toggle_pause():
    global is_pause
    is_pause = not is_pause
    if is_pause:
        btn_pause.config(text="继续播放")
    else:
        btn_pause.config(text="暂停动画")

# 重新播放
def restart_animation():
    if is_running:
        return
    clear_all_scene()
    draw_bus()
    threading.Thread(target=run_animation, daemon=True).start()

# 底部按钮
control_frame = tk.Frame(root)
control_frame.pack(pady=10)

btn_start = tk.Button(control_frame, text="开始动画", font=font_btn, bg="#63b3ed", width=14,
                      command=lambda: threading.Thread(target=run_animation, daemon=True).start())
btn_start.grid(row=0, column=0, padx=12)

btn_pause = tk.Button(control_frame, text="暂停动画", font=font_btn, bg="#f6e05e", width=14, command=toggle_pause)
btn_pause.grid(row=0, column=1, padx=12)

btn_restart = tk.Button(control_frame, text="重新播放", font=font_btn, bg="#68d391", width=14, command=restart_animation)
btn_restart.grid(row=0, column=2, padx=12)

draw_bus()
root.mainloop()
