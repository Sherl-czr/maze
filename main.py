
import pygame
import config
from game_manager import GameManager
from draw_text import draw_text
pygame.init()
pygame.mixer.init()  #　初始化声音

screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
clock = pygame.time.Clock()

pygame.mixer_music.load("static/sounds/bgm.wav")
pygame.mixer_music.set_volume(0.1)
pygame.mixer_music.play(-1)  # 参数-1表示循环播放
game_manager = GameManager(screen, 1)

success_time = -1
success_finished = False  # 是否已经通关
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # 如果已经通关，按下任意键退出
        elif success_finished and event.type == pygame.KEYDOWN:
            running = False
    # 先判断是否结束，没结束的时候，执行else。
    if success_finished:
        screen.fill("black")
        draw_text(screen, "Win!", 200, config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2)
    else:
        if success_time >= 0:
            if pygame.time.get_ticks() - success_time > 2000:
                has_next = game_manager.next_level()
                if not has_next:
                    success_finished = True
                    continue

                success_time = -1
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")
        if game_manager.update():
            success_time = pygame.time.get_ticks()
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(config.FPS)  # limits FPS to 60

pygame.quit()