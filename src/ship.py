import pygame

image_path = "../resources/images/"
image_name = "ship.bmp"


class Ship:
    """
    - 管理飞船的类
    """

    def __init__(self, ai_game):
        """
        - 初始化飞船并设置其初始位置
        :param ai_game: 管理游戏资源和行为的实例
        """
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load(image_path + image_name)
        self.rect = self.image.get_rect()

        # 对于每艘新飞船，都将其放在屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom

        # 移动标志，分别表示上下左右
        self.moving = 4 * [False]

        # 在飞船的属性x,y中存储小数值
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        """
        - 根据移动标志调整飞船位置
        :return: None
        """
        # 上移
        if self.moving[0] and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        # 下移
        if self.moving[1] and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed
        # 左移
        if self.moving[2] and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        # 右移
        if self.moving[3] and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed

        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        """
        - 在指定位置绘制飞船
        :return: None
        """
        self.screen.blit(self.image, self.rect)
