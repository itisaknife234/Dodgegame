import streamlit as st
import pygame
import random
import numpy as np
from PIL import Image
import time

FPS = 60
MAX_WIDTH = 500
MAX_HEIGHT = 750

pygame.init()

# 화면 설정
screen = pygame.Surface((MAX_WIDTH, MAX_HEIGHT))

# 이미지 로드 (PIL을 사용하여 로드 후 Pygame으로 변환)
def load_image(path, size=None):
    try:
        img = Image.open(path).convert("RGBA")
        if size:
            img = img.resize(size, Image.LANCZOS)
        return pygame.image.frombuffer(img.tobytes(), img.size, "RGBA")
    except Exception as e:
        print(f"Error loading image {path}: {e}")
        return pygame.Surface((size if size else (50, 50)))

background = load_image("background.png", (MAX_WIDTH, MAX_HEIGHT))
player_image = load_image("miya.png", (60, 60))
enemy_image = load_image("Dong.png", (45, 45))
bonus_image = load_image("melon.png", (40, 40))

font = pygame.font.Font(None, 36)

def show_message(messages):
    st.text("\n".join(messages))

def player_move(keys, player, speed=5):
    if keys[pygame.K_RIGHT] and player.x < MAX_WIDTH - 40:
        player.x += speed
    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= speed

class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.image = player_image
        
    def draw(self):
        return screen.blit(self.image, (self.x, self.y))
    
    def move(self, pressed_keys):
        player_move(pressed_keys, self)

class Enemy():
    def __init__(self):
        self.x = random.randrange(0, MAX_WIDTH - 40)
        self.y = 50
        self.speed = random.randrange(10, 20)
        self.image = enemy_image
        
    def draw(self):
        return screen.blit(self.image, (self.x, self.y))
        
    def move(self, score):
        self.y += self.speed
        if self.y >= MAX_HEIGHT:
            self.y = 50
            self.x = random.randrange(0, MAX_WIDTH - 40)
            self.speed = random.randrange(7, 15) + (score // 500)

class BonusItem():
    def __init__(self):
        self.x = random.randrange(0, MAX_WIDTH - 30)
        self.y = -30
        self.speed = 5
        self.image = bonus_image
        
    def draw(self):
        return screen.blit(self.image, (self.x, self.y))
    
    def move(self):
        self.y += self.speed
        if self.y >= MAX_HEIGHT:
            self.y = -30
            self.x = random.randrange(0, MAX_WIDTH - 30)

def main():
    st.title("Dodge the POOP Game!")
    
    show_message(["Press any arrow key to START!", "Dodge the POOP Eat melon for BONUS"])

    player = Player(MAX_WIDTH // 2, MAX_HEIGHT - 60)
    enemies = [Enemy()]
    bonus_item = BonusItem()
    score = 0
    clock = pygame.time.Clock()
    
    # Streamlit 화면 업데이트를 위한 while loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        pressed_keys = pygame.key.get_pressed()
        player.move(pressed_keys)
        
        screen.fill((255, 255, 255))  # 화면 초기화
        screen.blit(background, (0, 0))
        
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        
        player_rect = player.draw()
        
        if score >= 700 and len(enemies) == 1:
            enemies.append(Enemy())
        
        for enemy in enemies:
            enemy_rect = enemy.draw()
            enemy.move(score)
            if player_rect.colliderect(enemy_rect):
                show_message(["!Game Over!", f"Your score: {score}", "Restart the page to play again"])
                return
        
        bonus_rect = bonus_item.draw()
        bonus_item.move()
        
        if player_rect.colliderect(bonus_rect):
            score += 100
            bonus_item.y = -30
            bonus_item.x = random.randrange(0, MAX_WIDTH - 30)
        
        score += 1
        
        # Convert pygame surface to PIL Image for Streamlit display
        img = pygame.image.tostring(screen, "RGB")
        img = Image.frombytes("RGB", (MAX_WIDTH, MAX_HEIGHT), img)
        
        # Streamlit으로 이미지 표시
        st.image(img, use_container_width=True)
        
        # 프레임 속도 조절
        clock.tick(FPS)
        
        # Streamlit 인터페이스 갱신
        time.sleep(1 / FPS)
        st.experimental_rerun()

if __name__ == '__main__':
    main()
