import random
import tkinter as tk
import time


# 创建山脉生成器的类
class MountainGenerator:
    def __init__(self, canvas, interactive=False):
        self.canvas = canvas
        self.interactive = interactive
        self.points = []  # 存储山脉的点
        self.roughness = 0.25  # 初始粗糙度
        self.p0 = None  # 未使用
        self.iterations = 3  # 初始迭代次数

    # 设置粗糙度
    def set_roughness(self, roughness):
        self.roughness = roughness

    # 设置迭代次数
    def set_iterations(self, iterations):
        self.iterations = iterations

    # 计算两点之间的中点，并对其进行位移
    def displace_point(self, p1, p2):
        # 从参数p1和p2中提取x1, y1和x2, y2的坐标
        x1, y1 = p1
        x2, y2 = p2

        # 计算两个点的中间x坐标
        x = (x1 + x2) / 2

        # 计算p1和p2之间的距离（欧几里德距离）
        length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

        # 如果x1和x2之间的距离小于等于1，返回p1（不进行位移）
        if abs(x1 - x2) <= 1:
            return p1

        # 否则，计算一个新的y坐标，通过在原始y坐标上添加一个随机的偏移值
        # 偏移值在 -self.roughness 和 self.roughness 之间随机选择
        new_y = y1 + length * random.uniform(-self.roughness, self.roughness)

        # 返回新的坐标点 (x, new_y)
        return x, new_y

    # 执行中点位移算法
    def midpoint_displacement(self, p1, p2, iterations):
        # 基本情况：如果迭代次数已经为0，返回起点p1和终点p2
        if iterations == 0:
            return [p1, p2]

        # 计算中点pc，通过调用displace_point函数对p1和p2之间的中点进行位移
        pc = self.displace_point(p1, p2)

        # 如果位移后的中点等于起点p1，表示不需要再细分，直接返回起点p1和终点p2
        if pc == p1:
            return [p1, p2]
        else:
            # 递归调用，将问题拆分为两个子问题：
            # 1. 从p1到位移后的中点pc进行细分，迭代次数减一
            left_half = self.midpoint_displacement(p1, pc, iterations - 1)

            # 2. 从位移后的中点pc到p2进行细分，迭代次数减一
            right_half = self.midpoint_displacement(pc, p2, iterations - 1)

            # 返回两个子问题的结果连接起来，中间插入位移后的中点pc
            return left_half + [pc] + right_half

    # 交互式中点位移，用于可视化生成山脉的过程
    def interactive_midpoint_displacement(self, p1, p2, sleep=0.1):
        # 初始化一个点列表，开始时包含起点p1和终点p2
        self.points = [p1, p2]

        # 初始化标志变量flag为True，用于控制迭代循环
        flag = True

        # 在GUI上绘制初始线段，颜色为黑色
        self.canvas.create_line(self.points, fill="black")

        # 更新GUI显示
        self.canvas.update()

        # 暂停一段时间，以便观察初始线段
        time.sleep(sleep)

        # 进入循环，不断进行中点位移并更新GUI显示
        while flag:
            # 复制当前点列表，以便在迭代中修改
            points_new = self.points.copy()

            # 对当前点列表中的每对相邻点进行中点位移操作
            for i in range(len(self.points) - 1):
                pc = self.displace_point(self.points[i], self.points[i + 1])

                # 如果位移后的中点pc等于当前点中的起点，表示不需要再细分，退出循环
                if pc == self.points[i]:
                    flag = False
                    continue

                # 更新新的点列表，将位移后的中点pc插入到适当的位置
                points_new = points_new[:i + 1] + [pc] + points_new[i + 1:]

            # 更新当前点列表为新的点列表
            self.points = points_new

            # 在GUI上绘制新的线段，颜色为黑色
            self.canvas.create_line(self.points, fill="black")

            # 更新GUI显示
            self.canvas.update()

            # 暂停一段时间，以便观察迭代过程
            time.sleep(sleep)

        # 循环结束后，打印 "Finished" 表示生成过程完成
        print("Finished")

    # 重置画布
    def reset_code(self):
        # 使用GUI画布的delete方法，删除所有在画布上的图形元素，"all"表示删除所有
        self.canvas.delete("all")

        # 将对象的属性 self.points 重置为空列表，用于存储点坐标
        self.points = []

    # 生成山脉
    def build_mountains(self):
        # 重置画布和点列表
        self.reset_code()

        # 随机生成两个山峰的高度
        h1 = random.randint(100, 400)
        h2 = random.randint(100, 400)

        # 定义山峰的x坐标
        xh1 = 6
        xh2 = 994

        # 在画布上创建表示山峰的红色圆形点
        self.canvas.create_oval(xh2 - 3, h2 - 3, xh2 + 3, h2 + 3, fill="red", outline='black')

        # 将山峰的坐标添加到点列表中
        self.points.append([xh1, h1])
        self.points.append([xh2, h2])

        # 根据是否交互模式，选择不同的方法生成山脉
        if self.interactive:
            # 在交互模式下，使用 interactive_midpoint_displacement 方法生成山脉
            self.interactive_midpoint_displacement(self.points[0], self.points[1])
        else:
            # 在非交互模式下，使用 midpoint_displacement 方法生成山脉
            self.points = self.midpoint_displacement(self.points[0], self.points[1], self.iterations)
            for i in range(len(self.points) - 1):
                # 在画布上绘制连接点的线段
                self.canvas.create_line(self.points[i][0], self.points[i][1], self.points[i + 1][0],
                                        self.points[i + 1][1])


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Mountain Generator")

    canvas = tk.Canvas(root, width=1000, height=600)
    canvas.pack()

    generator = MountainGenerator(canvas, interactive=True)  # 设置 interactive 为 False 以使用非交互模式

    # 创建生成山脉按钮
    btn_generate = tk.Button(root, text="生成山脉", command=generator.build_mountains)
    btn_generate.pack(side="right")

    # 创建重置画布按钮
    btn_reset = tk.Button(root, text="重置画布", command=generator.reset_code)
    btn_reset.pack(side="right")

    r = tk.DoubleVar()
    r.set(0.4)

    label = tk.Label(root, text="粗糙度: 0.25")
    label.pack(side="left")

    # 创建粗糙度调节滑块
    scale = tk.Scale(root, from_=0, to=1.0, resolution=0.01, orient="horizontal", variable=r)
    scale.pack(side="left")

    # 迭代次数输入框
    iterations_label = tk.Label(root, text="迭代次数:")
    iterations_label.pack(side="left")
    iterations_entry = tk.Entry(root)
    iterations_entry.pack(side="left")
    iterations_entry.insert(0, "3")  # 设置默认迭代次数


    # 确认按钮，用于设置迭代次数
    def set_iterations():
        try:
            iterations = int(iterations_entry.get())
            generator.set_iterations(iterations)
        except ValueError:
            pass


    # 确认按钮
    iterations_button = tk.Button(root, text="确认", command=set_iterations)
    iterations_button.pack(side="left")

    root.mainloop()
