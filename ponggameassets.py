import pygame
import math

class playerpaddle:
    def __init__(self,x,screen_y):
        self.screen_y = screen_y
        self.width = 10
        self.length = 60
        self.speed = 5
        self.movement_y = 0
        self.sprite = pygame.Rect(x-self.width, self.screen_y // 2 - self.length // 2, self.width, self.length)
    def handleevents(self,up,down):
        self.movement_y = 0
        if up and self.sprite.top > 0:
            self.sprite.y -= self.speed
            self.movement_y = -self.speed
        if down and self.sprite.bottom < self.screen_y:
            self.sprite.y += self.speed
            self.movement_y = self.speed

class botpaddle:
    def __init__(self,x,screen_x,screen_y):
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.width = 12
        self.length = 72
        self.speed = 5
        self.movement_y = 0
        self.sprite = pygame.Rect(x-self.width, self.screen_y // 2 - self.length // 2, self.width, self.length)
    def handleai(self,ball1):
        if ball1.speed_x * ((self.screen_x/2-self.sprite.x)/abs(self.screen_x/2-self.sprite.x)) < 0:
            time_to_reach_paddle = (self.sprite.x - ball1.sprite.x) / ball1.speed_x
            predicted_ball_y = ball1.sprite.y + ball1.speed_y * time_to_reach_paddle
            target_y = predicted_ball_y
            while target_y < 0 or target_y > self.screen_y:
                if target_y < 0:
                    target_y = -target_y
                else:
                    target_y = 2 * self.screen_y - target_y
            target_y -= target_y%self.speed
            self.movement_y = 0
            if abs(self.sprite.centery - target_y) > self.length/3:
                if self.sprite.centery > target_y and self.sprite.top > 0:
                    self.sprite.y -= min(self.speed, self.sprite.top)
                    self.movement_y = -self.speed
                elif self.sprite.centery < target_y and self.sprite.bottom < self.screen_y:
                    self.sprite.y += min(self.speed,self.screen_y-self.sprite.bottom)
                    self.movement_y = self.speed

class ball:
    def __init__(self, screen_x, screen_y):
        self.lost = False
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.radius = 10
        self.speed_x = -3
        self.speed_y = 3
        self.speedaddpercollision = 0.1
        self.accel = 0
        self.max_speed = 24
        self.x = self.screen_x // 2 - self.radius // 2
        self.y = self.screen_y // 2 - self.radius // 2
        self.sprite = pygame.Rect(self.screen_x // 2 - self.radius // 2, self.screen_y // 2 - self.radius // 2, self.radius, self.radius)
        self.color = (255, 255, 255)
    def lose(self,score,wintext,players):
        if self.sprite.x < self.screen_x/2:
            score.score_right += 1
        else:
            score.score_left += 1
        if score.score_left > 10 or score.score_right > 10:
            self.lost = True
            self.speed_x = 0
            self.speed_y = 0
            if score.score_left > 10:
                wintext.display(self.screen, self.screen_x, self.screen_y, "Left Wins", (55,255,55))
            else:
                wintext.display(self.screen, self.screen_x, self.screen_y, "Right Wins", (255,55,55))
        if not self.lost:
            pygame.mixer.Sound(r"C:\Users\djuma\OneDrive\Documents\CS\DEV\Python\Pygame\Pong\assets\explosion.wav").play()
            self.x = self.screen_x // 2 - self.radius // 2
            self.y = self.screen_y // 2 - self.radius // 2
            self.sprite.x = self.x
            self.sprite.y = self.y
            self.speed_x = -3
            self.speed_y = 3
            for playerspeedreset in players:
                playerspeedreset.speed = 5

    def collisioncheck(self, players, wintext,score):
        if not self.lost:
            for player in players:
                if self.sprite.colliderect(player.sprite):
                    if player.sprite.x < self.screen_x / 2:
                        self.speed_x = -abs(self.speed_x)
                        pygame.mixer.Sound(r"C:\Users\djuma\OneDrive\Documents\CS\DEV\Python\Pygame\Pong\assets\hitHurt.wav").play()
                    else:
                        self.speed_x = abs(self.speed_x)
                        pygame.mixer.Sound(r"C:\Users\djuma\OneDrive\Documents\CS\DEV\Python\Pygame\Pong\assets\hitHurt.wav").play()
                    self.accel = 0
                    self.speed_x *= -1
                    self.speed_x += (self.speed_x / abs(self.speed_x)) * self.speedaddpercollision
                    self.accel = player.movement_y / abs(self.speed_x * 30)
                    self.speed_y += (self.speed_y / abs(self.speed_y) + ((player.sprite.y + player.length / 2) - (self.sprite.y + self.radius)) / 30) * self.speedaddpercollision
                    for playerspeedincrement in players:
                        if self.speed_x > 0 and self.speed_y > 0:
                            playerspeedincrement.speed = max(8,8 + abs(self.speed_y/self.speed_x))
            if self.sprite.top <= 0:
                if self.speed_y < 0:
                    pygame.mixer.Sound(r"C:\Users\djuma\OneDrive\Documents\CS\DEV\Python\Pygame\Pong\assets\hitHurt1.wav").play()
                    self.speed_y = abs(self.speed_y)
                    self.accel = 0
            if self.sprite.bottom >= self.screen_y:
                if self.speed_y > 0:
                    pygame.mixer.Sound(r"C:\Users\djuma\OneDrive\Documents\CS\DEV\Python\Pygame\Pong\assets\hitHurt1.wav").play()
                    self.speed_y = -abs(self.speed_y)
                    self.accel = 0
            if self.sprite.right >= self.screen_x:
                self.lose(score,wintext,players)
            if self.sprite.left <= 0:
                self.lose(score,wintext,players)

    def handleevents(self, players, wintext, screen,score):
        if not self.lost:
            self.screen = screen
            self.speed_y += self.accel
            self.speed_x += abs(self.accel / 2) * (self.speed_x / abs(self.speed_x))
            self.speed_x = min(self.max_speed, self.speed_x)
            self.speed_y = min(self.max_speed, self.speed_y)

            self.update_color()

            for _ in range(int(abs(math.ceil(self.speed_x)))):
                try:
                    self.x += self.speed_x / abs(self.speed_x)
                    self.y += self.speed_y / math.ceil(abs(self.speed_x))
                    self.sprite.x = self.x
                    self.sprite.y = self.y
                except:
                    self.x += 0
                    self.y += 0
                self.collisioncheck(players, wintext,score)


    def update_color(self):
        speed_ratio = min(pygame.math.Vector2(self.speed_x, self.speed_y).length() / self.max_speed, 1.0)
        self.color = (
        int(min(255,speed_ratio * 255)+(1-speed_ratio) * 255),
        int(min(255,(1-speed_ratio) * 255)),
        0)

class scorevalue:
    def __init__(self):
        self.score_left = 0
        self.score_right = 0

class wintext:
    def __init__(self):
        self.text = pygame.font.Font(None, 36).render('', True, (55, 255, 55))
        self.text_value = ""
    def display(self,screen,screen_x,screen_y,text,color):
        self.text = pygame.font.Font(None, 36).render(f'{text}', True, color)
        self.text_value = f"{text}"
        screen.blit(self.text,(screen_x//2 - self.text.get_width()//2,screen_y//2 - self.text.get_height()//2))

class scoretext:
    def __init__(self,score):
        self.text = pygame.font.Font(None, 36).render('', True, (55, 255, 55))
        self.text_value = f"{score.score_left} : {score.score_right}"
    def display(self,screen,screen_x,score):
        self.text = pygame.font.Font(None, 24).render(f'{score.score_left} : {score.score_right}', True, (255,255,255))
        self.text_value = f"{score.score_left} : {score.score_right}"
        screen.blit(self.text,(screen_x//2 - self.text.get_width()//2,30))