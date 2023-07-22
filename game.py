

class Snake:
    def __init__(self, length=3, head_color="Yellow", color="White") -> None:
        self.color = palette[color]
        self.head_color = palette[head_color]
        if screen_size[0] <= 2 * length or screen_size[1] <= 2 * length:
            raise Exception("The snake is too long for the screen.")
        # 添加蛇 蛇头在画面中央 身体按长度向左延申
        self.body = [[screen_size[0] // 2 - val, screen_size[1] // 2] for val in range(length)]
        # 蛇头运动方向 up down left right
        self.direction = "l"
        self.death = False
    
    def move(self):
        '''移动蛇头位置'''
        movement = {"u":(0, 1), "d":(0, -1), "l":(1, 0), "r":(-1, 0)}
        # 多加一格(现在会比之前长一格 后面再检测吃没吃到 如果没吃到再把身体最后一节删掉)
        self.body.insert(0,
                        [self.body[0][0] + movement[self.direction][0],
                         self.body[0][1] + movement[self.direction][1]])
        # 如果撞到自己或者撞墙了游戏结束
        if self.body[0] in self.body[1:] or self.body[0][0] not in range(screen_size[0]) or\
              self.body[0][1] not in range(screen_size[1]):
            self.death = True

    def turn(self, key):
        if self.direction in ("u", "d"):
            if key == "a":
                self.direction = "r"
                return True
            elif key == "d":
                self.direction = "l"
                return True
        else:
            if key == "w":
                self.direction = "u"
                return True
            elif key == "s":
                self.direction = "d"
                return True
            


def new_fruit(snake, color="Red"):
    from random import random
    fruit = [int(random() * screen_size[0]), int(random() * screen_size[1])]
    while fruit in snake.body:
        fruit = [int(random() * screen_size[0]), int(random() * screen_size[1])]
    return fruit+[palette[color]]



def display(snake, fruit, points):
    # 把光标移到最上面
    print("\033[F" * (screen_size[1] * 2))
    # 展示分数
    print(f"Points: {points}")
    # 创建一个屏幕大小的全是空的字典 {0:{0:"  ", 1:"  ", ...}, 1:{...}, ...}
    frame = [["  " for x in range(screen_size[0])] for y in range(screen_size[1])]
    for part in snake.body[1:]:
        frame[part[1]][part[0]] = snake.color
    frame[snake.body[0][1]][snake.body[0][0]] = snake.head_color
    frame[fruit[1]][fruit[0]] = fruit[2]
    for y in range(screen_size[1]-1, -1, -1):
        print("".join(frame[y]), end="██\n")
    print("██"*(screen_size[0] + 1))



def key_input():
    """用于捕获键盘输入"""
    from msvcrt import getwch
    global key
    while True:
        key = getwch()



palette = {
            "Black": "\033[30m██\033[0m",
            "Red": "\033[31m██\033[0m",
            "Green": "\033[32m██\033[0m",
            "Yellow": "\033[33m██\033[0m",
            "Blue": "\033[34m██\033[0m",
            "Magenta": "\033[35m██\033[0m",
            "Cyan": "\033[36m██\033[0m",
            "White": "\033[37m██\033[0m",
            "Bright Black": "\033[90m██\033[0m",
            "Bright Red": "\033[91m██\033[0m",
            "Bright Green": "\033[92m██\033[0m",
            "Bright Yellow": "\033[93m██\033[0m",
            "Bright Blue": "\033[94m██\033[0m",
            "Bright Magenta": "\033[95m██\033[0m",
            "Bright Cyan": "\033[96m██\033[0m",
            "Bright White": "\033[97m██\033[0m",
            "Dark Black": "\033[30;2m██\033[0m",
            "Dark Red": "\033[31;2m██\033[0m",
            "Dark Green": "\033[32;2m██\033[0m",
            "Dark Yellow": "\033[33;2m██\033[0m",
            "Dark Blue": "\033[34;2m██\033[0m",
            "Dark Magenta": "\033[35;2m██\033[0m",
            "Dark Cyan": "\033[36;2m██\033[0m",
            "Dark White": "\033[37;2m██\033[0m",
            }
from os import system
system("cls")
screen_size = [20, 20]
python = Snake()
fruit = new_fruit(python)
points = 0
# 用另一个线程接受键盘输入
from threading import Thread
Thread(target=key_input, daemon=True).start()
global key
key = None
# 控制一帧的时长
from time import sleep
while True:
    if python.turn(key):
        key = None
    # 运动一格 此时长度会多一节
    python.move()
    # 吃到果子
    if python.body[0] == fruit[:2]:
        fruit = new_fruit(python)
        points += 1
    # 没吃到果子 删掉最后一节 长度不变
    else:
        python.body.pop()
    if python.death:
        break
    display(python, fruit, points)
    sleep(1/5)
print("Game over")