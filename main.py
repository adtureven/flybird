# 引入模块
import pygame
import random
import os
# 基础设定，窗口的大小和帧率
W, H = 288, 512
FPS = 30      # 可以自行改动出其他效果。。。

pygame.init()
SCREEN = pygame.display.set_mode((W , H))
pygame.display.set_caption('flybird')
Clock = pygame.time.Clock()

# 将图片素材导入到字典中
IMAGE = {}
for image in os.listdir('flybird\image'):
    name, exten = os.path.splitext(image)
    path = os.path.join('flybird\image', image)
    IMAGE[name] = pygame.image.load(path)

# 导入声音素材
start = pygame.mixer.Sound('flybird\sound\start.wav')
flap = pygame.mixer.Sound('flybird\sound\\flap.wav')
hit = pygame.mixer.Sound('flybird\sound\hit.wav')
score = pygame.mixer.Sound('flybird\sound\score.wav')
die = pygame.mixer.Sound('flybird\sound\die.wav')
gao = pygame.mixer.Sound('flybird\sound\gao.wav')
js = pygame.mixer.Sound('flybird\sound\js.wav')  # 两个鬼畜声音


def main():
    while True:
        start.play()
        IMAGE['bg'] = IMAGE[random.choice(['day', 'night'])]   # 使背景出现白天和黑夜随机变化
        color = random.choice(['bird0', 'bird1', 'bird2'])
        IMAGE['bird'] = [IMAGE[color+'_0'], IMAGE[color+'_1'], IMAGE[color+'_2']]  # 和上一句一起实现小鸟颜色的随机变化
        pipe = IMAGE[random.choice(['pipe_up', 'pipe2_up'])]
        IMAGE['pipe'] = [pipe, pygame.transform.flip(pipe, False, True)]   # 实现水管两种颜色的变换
        menu_window()
        result = game_window()
        end_window(result)


def menu_window():    # 设置游戏一开始的画面
    land_gap = IMAGE['land'].get_width()-W    # 定义land图片的宽度和窗口宽度的差
    land_x = 0     # 将land图片的横坐标设为0

    bird_y = 240     # 设定鸟的纵坐标的值
    bird_y_vel = 1     # 将鸟每一帧纵坐标变化设为1
    bird_y_range = [bird_y-8, bird_y+8]    # 将鸟的纵坐标位置变化固定在一个范围内

    id = 0
    frame = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1]      # 设定小鸟按帧变化依次出现的图片编号
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return                # 设置游戏的操作键和相应的反应

        land_x -= 4      # 为了使地面动起来，每次循环将它的横坐标-4
        if land_x <= -land_gap:
            land_x = 0      # 如果图片快要移出窗口，就将它的横坐标重新拉回的0

        bird_y = bird_y+bird_y_vel      # 小鸟的纵坐标等于它与变化量的和
        if bird_y < bird_y_range[0] or bird_y > bird_y_range[1]:
            bird_y_vel *= -1         # 若小鸟的纵坐标将要跳出限定的范围内，就改变它的运动方向，使其往相反的方向运动

        id += 1    # 图片的编号依次加一
        id %= len(frame)   # 若图片的编号超出给的的frame的长度，就重新从头取图片

        SCREEN.blit(IMAGE['bg'], (0, 0))
        SCREEN.blit(IMAGE['title'], (52, 80))
        SCREEN.blit(IMAGE['text_ready'], (45, 170))
        SCREEN.blit(IMAGE['land'], (land_x, 400))
        SCREEN.blit(IMAGE['tap'], (85, 250))
        SCREEN.blit(IMAGE['bird'][frame[id]], (80, bird_y))    # 在窗口中依次在给定的位置显示出各个图片

        pygame.display.update()     # 刷新窗口屏幕
        Clock.tick(FPS)          # 两帧动画之间的时间差


def game_window():         # 游戏开始啦！！

    flap.play()           # 下落的声音播放
    land_gap = IMAGE['land'].get_width()-W
    land_x = 0       # 和前面窗口一样要是地面动起来

    bird = Bird(80, 240)

    distance = 150        # 设置前后两个柱子之间的距离
    pipe_gap = 100         # 设置上下两个柱子之间的间隙
    n_pairs = 4
    pipes = []          # 将水管放入一个列表中
    for i in range(n_pairs):      # 取随机数使每根柱子的高度发生变化
        pipe_y = random.randint(int(H*0.3), int(H*0.7))
        pipe_up = Pipe(288+i*distance, pipe_y, True)       # 调用Pipe类
        pipe_down = Pipe(288 + i * distance, pipe_y-pipe_gap, False)
        pipes.append(pipe_up)       # 在列表中加入pipe-up对象
        pipes.append(pipe_down)

    while True:
        Flap = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Flap = True
                    flap.play()               # 同上

        land_x -= 4
        if land_x <= -land_gap:
            land_x = 0                   # 同上

        bird.update(Flap)

        first_pipe_up = pipes[0]         # 设定第一根向上得水管图片
        first_pipe_down = pipes[1]       # 第一根向下的
        if first_pipe_up.rect.right < 0:
            pipes.remove(first_pipe_up)
            pipes.remove(first_pipe_down)          # 若第一根水管已经移出窗口，就将他们从列表中移走
            pipe_y = random.randint(int(H * 0.3), int(H * 0.7))
            new_pipe_up = Pipe(first_pipe_up.rect.x + n_pairs*distance, pipe_y, True)
            new_pipe_down = Pipe(first_pipe_down.rect.x + n_pairs * distance, pipe_y-pipe_gap, False)
            pipes.append(new_pipe_down)
            pipes.append(new_pipe_up)          # 前面的水管出去之后，加入新水管
            del first_pipe_up, first_pipe_down           # 删除这两个变量的定义

        for pipe in pipes:
            pipe.update()       # 进行刷新

        if bird.rect.y < 0 or bird.rect.y > 400:
            hit.play()
            die.play()
            result = {'bird': bird, 'pipe': pipe}
            return result                 # 若鸟撞到上面或撞到地面是结束游戏，并发出相应的音效

        for pipe in pipes:          # 碰撞检测
            r_to_l = max(bird.rect.right, pipe.rect.right)-min(bird.rect.left, pipe.rect.left)
            b_to_t = max(bird.rect.bottom, pipe.rect.bottom)-min(bird.rect.top, pipe.rect.top)
            if r_to_l < bird.rect.width + pipe.rect.width-10 and b_to_t < bird.rect.height + pipe.rect.height-10:
                hit.play()        # 上一句思想主要是判断两个图片有无重叠的面积，通过重叠后总宽和各自宽之和进行比较，-10纯纯只是增加体验
                die.play()
                result = {'bird': bird, 'pipe': pipe}
                return result        # 撞到柱子之后的相应音效

        first_pipe_up = pipes[0]
        if (bird.rect.left + first_pipe_up.x_vel) < first_pipe_up.rect.centerx < bird.rect.left:
            score.play()         # 判定得分并响起得分的声音，除以10纯粹为了鬼畜的声音

        SCREEN.blit(IMAGE['bg'], (0, 0))
        for pipe in pipes:
            SCREEN.blit(pipe.image, pipe.rect)
        SCREEN.blit(IMAGE['land'], (land_x, 400))

        SCREEN.blit(bird.image, bird.rect)
        pygame.display.update()
        Clock.tick(FPS)            # 显示图片并且刷新窗口屏幕


def end_window(result):    # 结束界面，大体和前面差不多，就不一一叙述了

    land_gap = IMAGE['land'].get_width()-W
    land_x = 0

    bird = result['bird']
    pipes = result['pipe']

    id = 0
    frame = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

        bird.go_die()

        land_x -= 4
        if land_x <= -land_gap:
            land_x = 0

        id += 1
        id %= len(frame)

        SCREEN.blit(IMAGE['bg'], (0, 0))
        SCREEN.blit(IMAGE['land'], (land_x, 400))
        SCREEN.blit(IMAGE['text_game_over'], (45, 170))
        SCREEN.blit(bird.image, bird.rect)
        pygame.display.update()
        Clock.tick(FPS)


class Bird:  # 引入鸟的类

    def __init__(self, x, y):
        self.frames = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1]
        self.id = 0
        self.images = IMAGE['bird']
        self.image = self.images[self.frames[self.id]]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y      # 鸟的横纵坐标
        self.y_vel = -10
        self.max_y_vel = 10   # 速度最大的改变量
        self.gravity = 1     # 鸟重力加速度
        self.rou = 45        # 鸟操作时角度的变化
        self.max_rou = -28
        self.rou_vel = -3
        self.y_vel_after_flap = -10
        self.rou_after_flap = 45

    def update(self, Flap = False):    # 定义刷新函数

        if Flap:
            self.y_vel = self.y_vel_after_flap
            self.rou = self.rou_after_flap

        self.y_vel = min(self.y_vel + self.gravity, self.max_y_vel)
        self.rect.y += self.y_vel
        self.rou = max(self.rou+self.rou_vel, self.max_rou)

        self.id += 1
        self.id %= len(self.frames)
        self.image = self.images[self.frames[self.id]]
        self.image = pygame.transform.rotate(self.image, self.rou)

    def go_die(self):        # 定义鸟死时的函数，使其进行自由落体，并发生角度的改变
        if self.rect.y < 400:
            self.rect.y += self.max_y_vel
            self.rou = -90
            self.image = self.images[self.frames[self.id]]
            self.image = pygame.transform.rotate(self.image, self.rou)    # 使用pygame中的角度旋转函数


class Pipe:         # 引入Pipe类，并能改变水管的上下倒置，以及水管上下位置的变化
    def __init__(self, x, y, upwards=True):
        if upwards:
            self.image = IMAGE['pipe'][0]     # 0图片是水管正的
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.top = y
        else:
            self.image = IMAGE['pipe'][1]    # 1图片水管是倒立的
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.bottom = y
        self.x_vel = -4

    def update(self):     # 刷新函数
        self.rect.x += self.x_vel

main()