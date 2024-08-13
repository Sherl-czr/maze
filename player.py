import math
import pygame
import config
from utils.collided import collided_rect

class Player(pygame.sprite.Sprite):
    def __init__(self, center_x, center_y, forward_angle):
        super().__init__()
        self.width = 100
        self.height = 50
        self.forward_angle = 0  # 在游戏坐标系中，顺时针转动的角度

        self.image_source = pygame.image.load("static/images/car.png").convert()
        self.image = pygame.transform.scale(self.image_source, (self.width, self.height))
        self.image = pygame.transform.rotate(self.image_source, -self.forward_angle)
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        # rect 有x和y， 还有center, bottom, top, left, right.
        self.rect.center = (center_x, center_y)
        self.last_time = pygame.time.get_ticks()   # 返回当前时刻,单位是ms
        self.delta_time = 0

        self.move_velocity_limit = 300  # 移动速度的上限
        self.move_velocity = 0  # 当前的移动速度
        self.move_acc = 600  # 每秒将速度增加600个像素
        self.rotate_velocity_limit = 140  # 角速度上限
        self.rotate_velocity = 0  # 旋转角速度
        self.friction = 0.9  # 摩擦力的系数

        self.crash_sound = pygame.mixer.Sound("static/sounds/crash.mp3")
        self.crash_sound.set_volume(0.1)

        self.move_sound = pygame.mixer.Sound("static/sounds/move.mp3")
        self.move_sound.set_volume(0.5)
        self.move_sound_channel = pygame.mixer.Channel(7)


    # 更新每一帧的时间，当前时间减去上一个时间
    def update_delta_time(self):
        cur_time = pygame.time.get_ticks()
        self.delta_time = (cur_time - self.last_time) / 1000  # 毫秒转化为秒
        self.last_time = cur_time

    def input(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_UP]:
            self.move_velocity += self.move_acc * self.delta_time
            self.move_velocity = min(self.move_velocity, self.move_velocity_limit)
            if not self.move_sound_channel.get_busy():
                self.move_sound_channel.play(self.move_sound)
        elif key_pressed[pygame.K_DOWN]:
            self.move_velocity -= self.move_acc * self.delta_time
            self.move_velocity = max(self.move_velocity, -self.move_velocity_limit)
        else:
            self.move_velocity = int(self.move_velocity * self.friction)  # 以这个衰减的系数进行减少
            if not self.move_sound_channel.get_busy():
                self.move_sound_channel.stop()
        if key_pressed[pygame.K_RIGHT]:
            self.rotate_velocity = self.rotate_velocity_limit
        elif key_pressed[pygame.K_LEFT]:
            self.rotate_velocity = -self.rotate_velocity_limit
        else:
            self.rotate_velocity = 0

    def rotate(self, direction):
        self.forward_angle += self.rotate_velocity * self.delta_time
        self.image = pygame.transform.scale(self.image_source, (self.width, self.height))
        self.image = pygame.transform.rotate(self.image_source, -self.forward_angle)
        self.image.set_colorkey("black")
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def move(self, direction=1):
        if direction == 1 and abs(self.move_velocity) > 50:
            self.rotate(direction)   # 只有车在发动的时候才会发生转向
        vx = self.move_velocity * math.cos(math.pi * self.forward_angle / 180) * direction
        vy = self.move_velocity * math.sin(math.pi * self.forward_angle / 180) * direction
        self.rect.x += vx * self.delta_time
        self.rect.y += vy * self.delta_time
        if direction == -1 and abs(self.move_velocity) > 50:
            self.rotate(direction)

    # 撞墙了
    def crash(self):
        self.crash_sound.play()
        self.move(-1)  # 让车退回来
        if self.move_velocity >= 0:
            self.move_velocity = min(-self.move_velocity, -100)
        else:
            self.move_velocity = max(self.move_velocity, 100)

    def update(self):
        self.update_delta_time()
        self.input()
        self.move()
