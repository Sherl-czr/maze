import pygame
from player import Player
from wall import Wall

from utils.collided import collided_rect
# 使用这个类来帮助管理更新这两个对象即可。
class GameManager:
    def __init__(self, screen, level):
        self.screen = screen
        self.player = None
        self.walls = pygame.sprite.Group()
        wall = Wall(200, 200, 500, 5)
        self.load()

    def load_walls(self, walls):
        self.walls.empty()   #　清空
        for x, y, width, heigth in walls:
            wall = Wall(x, y, width, heigth)
            wall.add(self.walls)

    def load_player(self, center_x, center_y, forward_angle):
        if self.player:
            self.player.kill()
        self.player = Player(center_x, center_y, forward_angle)

    def load(self):     # 加载地图信息
        with open("static/maps/level1.txt", "r") as fin:
            walls_count = int(fin.readline())
            walls = []
            for i in range(walls_count):
                x, y, width, height = map(int, fin.readline().split())
                walls.append((x, y, width, height))
            self.load_walls(walls)
            center_x, center_y, forward_angle = map(int, fin.readline().split())
            self.load_player(center_x, center_y, forward_angle)

    def update(self):
        if self.player:
            self.player.update()
        self.check_collision()
        self.screen.blit(self.player.image, self.player.rect)
        self.walls.update()
        self.walls.draw(self.screen)

    def check_collision(self):
        if pygame.sprite.spritecollide(self.player, self.walls, False, collided_rect):
            self.player.crash()
