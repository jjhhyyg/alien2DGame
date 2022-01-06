import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """
    - 管理游戏资源和行为的类
    """

    def __init__(self):
        """
        - 初始化游戏并创建游戏资源
        """
        # 初始化背景设置
        pygame.init()
        self.settings = Settings()

        # self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # 飞船实例
        self.ship = Ship(self)

        # 子弹组
        self.bullets = pygame.sprite.Group()

        # 外星人组
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    def _create_fleet(self):
        """
        - 创建外星人群
        :return: None
        """
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - 2 * alien_width
        available_space_y = self.settings.screen_height - 3 * alien_height - self.ship.rect.height
        number_aliens_x = available_space_x // (2 * alien_width)
        number_rows = available_space_y // (2 * alien_height)
        # 创建外星人群
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """
        - 创建一个外星人并将其放在当前行
        :param alien_number: 外星人数量
        :return: None
        """
        alien = Alien(self)
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def run_game(self):
        """
        - 开始游戏的主循环
        :return: None
        """
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()

    def _check_events(self):
        # 监视键盘和鼠标事件
        """
        - pygame.event.get()方法
        - 返回一个列表，其中包含它在上一次被调用之后发生的所有事件
        - 所有键盘和鼠标事件都将导致这个for循环运行
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """相应按键"""
        if event.key == pygame.K_UP:
            self.ship.moving[0] = True
        if event.key == pygame.K_DOWN:
            self.ship.moving[1] = True
        if event.key == pygame.K_LEFT:
            self.ship.moving[2] = True
        if event.key == pygame.K_RIGHT:
            self.ship.moving[3] = True
        # 退出游戏
        if event.key == pygame.K_ESCAPE:
            sys.exit()
        # 发射子弹
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """响应松开"""
        if event.key == pygame.K_UP:
            self.ship.moving[0] = False
        if event.key == pygame.K_DOWN:
            self.ship.moving[1] = False
        if event.key == pygame.K_LEFT:
            self.ship.moving[2] = False
        if event.key == pygame.K_RIGHT:
            self.ship.moving[3] = False

    def _check_fleet_edges(self):
        """
        - 有外星人到达边缘时采取相应的措施
        :return: None
        """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """
        - 将整群外星人下移，并改变它们的方向
        :return: None
        """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_bullet_alien_collisions(self):
        """
        - 响应子弹和外星人碰撞
        :return: None
        """
        # 检查是否有子弹击中外星人，如果是，就删除相应的子弹和外星人
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            # 删除现有的子弹并新建一群外星人
            self.bullets.empty()
            self._create_fleet()

    def _fire_bullet(self):
        """
        - 创建一颗子弹，并将其加入编组bullets中
        :return: None
        """
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """
        - 更新子弹的位置并删除消失的子弹
        - for循环要求遍历的列表长度不变，所以要遍历bullets组的副本，否则遍历的列表长度会变
        :return: None
        """
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0 or bullet.rect.right <= 0 \
                    or bullet.rect.top >= self.settings.screen_height \
                    or bullet.rect.left >= self.settings.screen_width:
                self.bullets.remove(bullet)
        self.bullets.update()
        # print(len(self.bullets))
        self._check_bullet_alien_collisions()

    def _update_screen(self):
        """
        - 更新屏幕上的图像，并切换到新屏幕
        - fill()方法
        - 只接受一个实参：一种颜色
        :return:
        """
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        # 让最近绘制的屏幕可见
        pygame.display.flip()

    def _update_aliens(self):
        """
        - 检查是否有外星人位于屏幕边缘
        - 更新外星人群中所有外星人的位置
        :return: None
        """
        self._check_fleet_edges()
        self.aliens.update()


if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
