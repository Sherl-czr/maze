
import pygame

# 初始化Pygame
pygame.init()

# 设置窗口尺寸
screen = pygame.display.set_mode((800, 600))

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# 定义Tile尺寸
TILE_SIZE = 40

# 定义地图（0表示空白，1表示墙壁）
map_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# 游戏主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 填充背景
    screen.fill(WHITE)

    # 绘制地图
    for row_index, row in enumerate(map_data):
        for col_index, tile in enumerate(row):
            if tile == 1:
                pygame.draw.rect(
                    screen,
                    BLACK,
                    pygame.Rect(col_index * TILE_SIZE, row_index * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                )
            else:
                pygame.draw.rect(
                    screen,
                    GREEN,
                    pygame.Rect(col_index * TILE_SIZE, row_index * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                )

    # 刷新屏幕
    pygame.display.flip()

# 退出Pygame
pygame.quit()