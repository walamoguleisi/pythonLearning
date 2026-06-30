import tkinter as tk
import time

# 窗口初始化
root = tk.Tk()
root.title("一年级数学：公交车人数倒推动画")
root.geometry("900x600")
root.resizable(False, False)
canvas = tk.Canvas(root, width=900, height=600, bg="#f0f8ff")
canvas.pack()

# 文字样式
font_big = ("微软雅黑", 22, "bold")
font_mid = ("微软雅黑", 18)
font_small = ("微软雅黑", 14)

# 绘制公交车基础图形
def draw_bus():
    # 车身
    canvas.create_rectangle(100, 200, 800, 420, fill="#4299e1", outline="black", width=3)
    # 车窗
    for i in range(5):
        x1 = 130 + i * 120
        canvas.create_rectangle(x1, 220, x1+100, 300, fill="white", outline="black")
    # 车轮
    canvas.create_oval(180, 410, 260, 490, fill="#333333")
    canvas.create_oval(640, 410, 720, 490, fill="#333333")
    canvas.create_text(450, 160, text="公交车人数问题动画", font=("微软雅黑", 24, "bold"), fill="#2c5282")

# 清除所有文字小人
def clear_all():
    canvas.delete("person")
    canvas.delete("text")
    root.update()

# 画小人标记
def draw_person(x, y, tag="person", color="#e53e3e"):
    # 头
    canvas.create_oval(x, y, x+22, y+22, fill=color, tags=tag)
    # 身体
    canvas.create_line(x+11, y+22, x+11, y+48, fill=color, width=3, tags=tag)
    # 手脚
    canvas.create_line(x, y+32, x+22, y+32, fill=color, width=3, tags=tag)
    canvas.create_line(x+11, y+48, x, y+62, fill=color, width=3, tags=tag)
    canvas.create_line(x+11, y+48, x+22, y+62, fill=color, width=3, tags=tag)

# 延时函数
def sleep(sec):
    root.update()
    time.sleep(sec)

# 主动画流程
def run_animation():
    draw_bus()
    sleep(1)

    # 步骤1：出示题目
    canvas.create_text(450, 80, text="题目：车上原来有一些人，到站下去5人，上来3人，现在车上13人，原来有几人？",
                       font=font_mid, fill="#1a202c", tags="text")
    sleep(3)
    clear_all()
    draw_bus()

    # 步骤2：展示最终状态：现在车上13个小人
    canvas.create_text(450, 80, text="第一步：现在车上有13人", font=font_big, fill="#2b6cb0", tags="text")
    pos_x = 140
    for i in range(13):
        draw_person(pos_x, 230)
        pos_x += 48
        sleep(0.15)
    sleep(2)

    # 步骤3：倒推：先减去上车的3人（绿色小人是刚上车的，下车消失）
    canvas.create_text(450, 115, text="倒推1：把后来上车的3个人请下车（减去3）", font=font_mid, fill="#2f855a", tags="text")
    # 标记最后3个小人绿色，然后擦掉
    for i in range(3):
        draw_person(140 + 48*(10+i), 230, color="#38a169")
    sleep(2)
    canvas.delete("person")
    # 只剩10个人
    pos_x = 140
    for i in range(10):
        draw_person(pos_x, 230)
        pos_x += 48
    canvas.create_text(450, 530, text="算式：13 - 3 = 10", font=font_big, fill="green", tags="text")
    sleep(3)

    # 步骤4：倒推第二步：把之前下车的5个人加回来（红色补上5人）
    canvas.create_text(450, 115, text="倒推2：把之前下车的5个人接回来（加上5）", font=font_mid, fill="#c53030", tags="text")
    canvas.delete("text")
    canvas.create_text(450, 80, text="倒推2：把之前下车的5个人接回来（加上5）", font=font_mid, fill="#c53030", tags="text")
    # 新增5个红色小人
    for i in range(5):
        draw_person(140 + 48*(10+i), 230, color="#e53e3e")
        sleep(0.3)
    canvas.create_text(450, 530, text="算式：10 + 5 = 15", font=font_big, fill="red", tags="text")
    sleep(3)

    # 步骤5：汇总完整算式，给出答案
    clear_all()
    draw_bus()
    canvas.create_text(450, 70, text="完整解题过程（倒推法）", font=font_big, fill="#742a2a", tags="text")
    canvas.create_text(450, 130, text="现在人数：13人", font=font_mid, tags="text")
    canvas.create_text(450, 170, text="先去掉上车的3人：13 - 3 = 10", font=font_mid, fill="green", tags="text")
    canvas.create_text(450, 210, text="再加回下车的5人：10 + 5 = 15", font=font_mid, fill="red", tags="text")
    canvas.create_text(450, 280, text="综合算式：13 - 3 + 5 = 15", font=("微软雅黑", 26, "bold"), fill="#2c5282", tags="text")
    canvas.create_text(450, 360, text="答：车上原来有15人", font=("微软雅黑", 28, "bold"), fill="#d69e2e", tags="text")

    # 画出15个小人表示原来人数
    pos_x = 130
    for i in range(15):
        draw_person(pos_x, 320)
        pos_x += 42
        sleep(0.1)
    sleep(2)
    canvas.create_text(450, 520, text="动画演示结束，可以关闭窗口", font=font_small, fill="#4a5568", tags="text")

# 点击窗口任意位置开始动画
def start_anim(event):
    btn.destroy()
    run_animation()

# 开始按钮
btn = tk.Button(root, text="点击这里开始动画讲解", font=font_big, bg="#63b3ed", width=25)
btn.place(x=280, y=520)
root.bind("<Button-1>", start_anim)

root.mainloop()
