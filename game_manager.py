import os

import pygame
from player import Player
from wall import Wall
from star import Star
from target import Target
from line import Line
from utils.collided import collided_rect, collided_circle


# 使用这个类来帮助管理更新这两个对象即可。
class GameManager:
    def __init__(self, screen, level):
        self.screen = screen
        self.player = None
        self.walls = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.targets = pygame.sprite.Group()
        self.lines = pygame.sprite.Group()
        self.stars_count = 0
        self.targets_count = 0
        self.level = 1
        self.eat_stars_sound = pygame.mixer.Sound('static/sounds/eat_stars.wav')
        self.eat_stars_sound.set_volume(0.3)
        self.success_sound = pygame.mixer.Sound('static/sounds/success.wav')
        self.success_sound.set_volume(0.3)
        wall = Wall(200, 200, 500, 5)
        self.load()

    def load_lines(self, lines):
        self.lines.empty()
        for x, y, width, height in lines:
            line = Line(x, y, width, height)
            line.add(self.lines)

    def load_walls(self, walls):
        self.walls.empty()   # 清空
        for x, y, width, heigth in walls:
            wall = Wall(x, y, width, heigth)
            wall.add(self.walls)

    def load_targets(self, targets):
        self.targets.empty()
        for x, y in targets:
            target = Target(x, y)
            target.add(self.targets)

    def load_player(self, center_x, center_y, forward_angle):
        if self.player:
            self.player.kill()
        self.player = Player(center_x, center_y, forward_angle)

    def load_stars(self, stars):
        self.stars.empty()

        for x, y in stars:
            star = Star(x, y)
            star.add(self.stars)

    def load(self):     # 加载地图信息
        with open("static/maps/level%d.txt" % self.level, "r") as fin:
            walls_count = int(fin.readline())
            walls = []
            for i in range(walls_count):
                x, y, width, height = map(int, fin.readline().split())
                walls.append((x, y, width, height))
            self.load_walls(walls)

            self.stars_count = int(fin.readline())
            stars = []
            for i in range(self.stars_count):
                x, y = map(int, fin.readline().split())
                stars.append((x, y))

            self.load_stars(stars)

            self.targets_count = int(fin.readline())
            targets = []
            for i in range(self.targets_count):
                x, y = map(int, fin.readline().split())
                targets.append((x, y))
            self.load_targets(targets)

            center_x, center_y, forward_angle = map(int, fin.readline().split())
            self.load_player(center_x, center_y, forward_angle)
            # lines_count = int(fin.readline())
            # lines = []
            # for i in range(lines_count):
            #     x, y, width, height = map(int, fin.readline().split())
            #     lines.append((x, y, width, height))

            # self.load_lines(lines)

    def update(self):
        # self.lines.update()
        # self.lines.draw(self.screen)
        self.targets.update()
        self.targets.draw(self.screen)
        self.stars.update()
        self.stars.draw(self.screen)
        if self.player:
            self.player.update()

        self.screen.blit(self.player.image, self.player.rect)

        self.walls.update()
        self.walls.draw(self.screen)
        success = self.check_collision()
        return success

    def check_collision(self):
        if pygame.sprite.spritecollide(self.player, self.walls, False, collided_rect):
            self.player.crash()
        if pygame.sprite.spritecollide(self.player, self.stars, True, collided_circle):
            self.stars_count -= 1
            self.eat_stars_sound.play()
            # 让星星消失的函数是上边的这个collide里面的true。
        if self.stars_count == 0 and pygame.sprite.spritecollide(self.player, self.targets, True, collided_circle):
            self.success_sound.play()
            return True
        return False

    def next_level(self):
        self.level += 1
        if not os.path.isfile("static/maps/level%d.txt" % self.level):
            return False
        self.load()
        return True
