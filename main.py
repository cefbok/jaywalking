import pygame, sys
from settings import *
from player import Player
from cars import Car
from sprite import simpleSprites
from sprite import longSprites
from random import choice, randint

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2()
        self.bg = pygame.image.load('./Frogger/graphics/main/map.png').convert_alpha()
        self.fg = pygame.image.load('./Frogger/graphics/main/overlay.png').convert_alpha()

    def custom_draw(self):
        self.offset.x = player.rect.centerx - window_w / 2
        self.offset.y = player.rect.centery - window_h / 2
        display_surface.blit(self.bg, -self.offset)
        
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            display_surface.blit(sprite.image, offset_pos)
    
        display_surface.blit(self.fg, -self.offset)

# setup
pygame.init()
display_surface = pygame.display.set_mode((window_w, window_h))
pygame.display.set_caption("dont't die jaywalking")
clock = pygame.time.Clock()

# groups
all_sprites = AllSprites()
obstacle = pygame.sprite.Group()

# Sprite
player = Player((2062, 3274), all_sprites, obstacle)

# timer
car_timer = pygame.event.custom_type()
pygame.time.set_timer(car_timer, 50)
pos_list = []

font = pygame.font.Font(None, 50)
text_surf = font.render('You Won a Ticket!', True, 'White')
text_rect = text_surf.get_rect(center = (window_w / 2, window_h / 2))

# music
music = pygame.mixer.Sound('./Frogger/audio/music.mp3')
music.play(loops = -1)
music.set_volume(0.7)

#sprite setup
for file_name, pos_list in SIMPLE_OBJECTS.items():
    path = f'./Frogger/graphics/objects/simple/{file_name}.png'
    surf = pygame.image.load(path).convert_alpha()
    for pos in pos_list:
        simpleSprites(surf, pos, [all_sprites, obstacle])
for file_name, pos_list in LONG_OBJECTS.items():
    surf = pygame.image.load(f'./Frogger/graphics/objects/long/{file_name}.png').convert_alpha()
    for pos in pos_list:
        longSprites(surf, pos, [all_sprites, obstacle])


# game loop
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == car_timer:
            random_pos = choice(CAR_START_POSITIONS)
            if random_pos not in pos_list:
                pos_list.append(random_pos)
                position = (random_pos[0], random_pos[1] + randint(-8,8))
                Car(position, [all_sprites, obstacle])
            if len(pos_list) > 5:
                del pos_list[0]

    # delta time
    dt = clock.tick() / 1000
    
    # draw
    display_surface.fill('black')

    if  player.pos.y >= 1180:
        # update
        all_sprites.update(dt)
        #all_sprites.draw(display_surface)
        all_sprites.custom_draw()
    else:
        display_surface.fill('teal')
        display_surface.blit(text_surf, text_rect)

    # update / display frame
    pygame.display.update()