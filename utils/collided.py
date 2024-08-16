import pygame
import math

# 调整一遍我们的接触的面积和交互的位置。
def collided_rect(a, b):
    p = []
    for i, j in [(1, -1), (1, 1), (-1, 1), (-1, -1)]:
        t = pygame.Vector2(i * a.width / 2 * 0.9, j * a.height / 2 * 0.9).rotate(a.forward_angle)
        p.append(t + a.rect.center)  # t是偏移量，加上中心得到的是周围四个角的值
    for i in range(4):
        x = p[i]
        y = p[(i+1) % 4]
        if b.rect.clipline(x, y):  # 有交点，返回true。
            return True
    p.clear()
    for i, j in [(1, -1), (1, 1), (-1, 1), (-1, -1)]:
        t = pygame.Vector2(i * a.width / 2 , j * a.height / 2 * 0.2).rotate(a.forward_angle)
        p.append(t + a.rect.center)  # t是偏移量，加上中心得到的是周围四个角的值
    for i in range(4):
        x = p[i]
        y = p[(i + 1) % 4]
        if b.rect.clipline(x, y):  # 有交点，返回true。
            return True

    return False

def collided_circle(a, b):
    x1, y1 = a.rect.center
    x2, y2 = b.rect.center
    dx = x2 - x1
    dy = y2 - y1
    if math.sqrt(dx * dx + dy * dy) < 50:
        return True
    return False


